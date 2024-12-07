# Kubernetes Deployment for the demonstration

This document centralizes materials to deploy OWL demonstrations and solutions to a Kubernetes platform. As target cluster we will use Scaleway cloud provider kubernetes services. As a first solution, we will use IBU Insurance demo.

The goal is to deploy all the components in one command:

```sh
make deploy_all
```

For maintenance purpose, it is important to understand how each components are deployed:

* Deploy one Postgresql cluster using Postgres kubernetes operator: [Cloudnative PG](https://github.com/cloudnative-pg/cloudnative-pg). 
* Deploy the Data Manager service for the IBU Insurance demo.
* Deploy the demonstration ibu backend
* Deploy the owl front end

All of the commands used are added to a unique Makefile to simplify the deployment of a solution and hide some of the kubectl commands.

## A Kubernetes Playground

If you know nothing about Kubernetes, maybe start with [this official tutorial](https://kubernetes.io/docs/tutorials/). RedHat has also a very [good content](https://developers.redhat.com/products/openshift/overview). For ODM experts, it is mandatory to read [this git repo: Deploying IBM Operational Decision Manager on a Certified Kubernetes Cluster.](https://github.com/DecisionsDev/odm-docker-kubernetes)

For tutorial, we recommend using a local kubernetes like Minikube (See [installation guide](https://kubernetes.io/docs/tasks/tools/install-minikube)) or with [KinD](https://kind.sigs.k8s.io/docs/user/quick-start). For internet facing deployments, we use Scaleway.

### Tools needed

The following CLI are needed:

* helm [See installation instructions.](https://helm.sh/docs/intro/quickstart/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

The `.env` file with the different environment variables used by the OWL Backend for the different API Key secrets.

### Access to Scaleway

To access Scaleway, there is one kubernetes cluster already created by the system administrator. Be sure to get the security tokens and the access username within the file named: `athena-demo_ibu_kubeconfig`, which is a kubeconfig specification manifest used to access the `athena-demo` cluster with write access to the `ibu` namespace. Normally this file can be saved under the `$HOME/.kube` folder. (If you have an existing `.kube/config` file to define existing Kubernetes contexts, then you may want to merge the  `athena-demo_ibu_kubeconfig` content into this `.kube/config` file, and then set the current context to `athena-demo`). 

Use this command to specify the kubectl context to use, so that all commands done with kubectl will go to the Scaleway cluster.

```sh
export KUBECONFIG=~/.kube/athena-demo_ibu_kubeconfig
```

* Verify you can access the Scaleway cluster, by listing the nodes within Kubernetes

```sh
$ kubectl get nodes 
NAME                                             STATUS   ROLES    AGE     VERSION
scw-athena-demo-infra-4c7f37b95e7a40d7b78375fb   Ready    <none>   4h55m   v1.30.2
scw-athena-demo-runners-a1fb1bcfe50647eabf642c   Ready    <none>   122m    v1.30.2
```

* Verify the namespaces

```sh
kubectl get  ns
```
The `ibu` namespace is the one used for the demonstration.

## Postgres deployment

For production deployment, it may be relevant to consider using a managed services to deploy Postgresql, like AWS RDS or [Scaleway managed database](https://www.scaleway.com/en/database/). In the current approach, we deploy Postgresql on k8s using an Operator. Operator automates the deployment and keeps it over time according to the specifications defined in the Customer Resource Definitions.

CloudNativePG has been designed by Postgres experts with Kubernetes administrators in mind. We recommend reading [this Postgres k8s operator introduction](https://github.com/cloudnative-pg/cloudnative-pg), you will find some good content about the value of this operator.

### Install Postgresql operator

The operator simplifies the management of Postgresql cluster, and automate the deployment and maintenance of the consistency between declarations and run time. The status of the Postgres cluster, is directly available in the Cluster resource, accessible through the Kubernetes API. 

See [source of information for operator installation.](https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/installation_upgrade.md). Verify in the future the release of the operator [here](https://github.com/cloudnative-pg/cloudnative-pg/releases).

* Deploy Postgresql operator 1.24.1

```sh
make deploy_postgres_operator
# Verify deployment of the operator
kubectl get deployment -n cnpg-system cnpg-controller-manager
```

### Define Postgresql cluster

There are multiple options to deploy Postgresql Cluster: we selected the deployment within a single kubernetes cluster using asynchronous streaming replication to manage multiple hot standby postgres server replicas. This will create 3 services for any applications to access Postgresql:

* -rw: applications connect only to the primary instance of the cluster
* -ro: applications connect only to hot standby replicas for read-only-workloads
* -r: applications connect to any of the instances for read-only workloads 

(Read more from [this article](https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/architecture.md#postgresql-architecture))

For application like the DataManager, it connects to the Postgres using the `rw service` via dns, using service.namespace names. The PostgreSQL operator generates two `basic-auth` type secrets for every PostgreSQL cluster it deploys:

1. [cluster name]-app 
1. [cluster name]-superuser

We uses the `-app` secrets to access to the DB cluster. 

* Deploy a Postgresql cluster with one active node (in fact a pod) and 2 backup nodes (pods)

[Good article](https://www.cncf.io/blog/2023/09/29/recommended-architectures-for-postgresql-in-kubernetes/) to get best practices and design considerations for PostgreSQL deployments in Kubernetes.

See the CRD for a 3-node PostgreSQL cluster, in the `postgresql` folder. The `make` target to deploy the cluster is:

```sh
make deploy_postgresql
```

* We can verify the 3 pods are started with:

```sh
kubectl get pods -n ibu
# output
athena-pg-cluster-1     1/1     Running   0          24d
athena-pg-cluster-2     1/1     Running   0          24d
athena-pg-cluster-3     1/1     Running   0          24d
```

* The 3 postgresql services 

```sh
kubectl get svc -n ibu
# output
athena-pg-cluster-r       ClusterIP      10.xx.xx.xx    5432/TCP         24d
athena-pg-cluster-ro      ClusterIP      10.xx.xx.xx   5432/TCP         24d
athena-pg-cluster-rw      ClusterIP      10.xx.xx.xx   5432/TCP         24d
```

* Get a deeper review of the cluster deployment:

```sh
kubectl describe cluster -n ibu
```

* The postgresql secrets:

```sh
kubectl get secrets -n ibu
# Verify the JDBC URI
kubectl get secret athena-pg-cluster-app -o jsonpath='{.data.jdbc-uri}' | base64 --decode
```

The Database servers are exposed only internally within the Kubernetes cluster. The service type is ClusterIP. The jdbc.url endpoint is used by the data manager for the demonstration.

## Deploy the DataManager

A helm chart is defined in the `ibu-data-mgr` folder. This microservice is a backend and should not be exposed to the internet, so it is also deployed with ClusterIP service.

To access the Postgresql cluster, in the same namespace, application needs the admin user name, its password and the jdbc connection URL. Those were defined during the Postgresql cluster deployment. The deployment has environment variables defined to use the postgresql secrets.

To deploy do the following command:

```sh
# First time to deploy
make  deploy_data_mgr
# Any changes to the values.yaml or deployment.yaml within the helm char folder can be propagated to the running pod via:
make upgrade_data_mgr
```

It should display a note explaining how to quickly test the access to the service using kubectl port forwarding command.

```sh
export POD_NAME=$(kubectl get pods --namespace ibu -l "app.kubernetes.io/name=ibu-data-mgr,app.kubernetes.io/instance=ibu-data-mgr" -o jsonpath="{.items[0].metadata.name}")
export CONTAINER_PORT=$(kubectl get pod --namespace ibu $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
kubectl --namespace ibu port-forward $POD_NAME 8080:$CONTAINER_PORT
```

The deployment descriptor is a helm template and defines the environment variables to use to access the database server. See the ./ibu-data-mgr/tamplates/deployments.yaml file

### Troubleshooting

If the pod is in state `CreateContainerConfigError`, use the pod description to get the error log: ` kubectl describe pod ibu-data-mgr`. 

## Deploy IBU backend

A helm chart is defined in the `ibu-backend` folder. To deploy using make:

```sh
make deploy_ibu_backend
# Or if already deployed
make upgrade_ibu_backend
```

* Verify the secrets in the container.

```sh
kubectl get secret ibu-dotenv -o jsonpath='{.data.\.env}'  | base64 --decode
kubectl get pods
kubectl exec -ti ibu-backend-8574d75f49-bcg24 -- env
```

The application is not exposed to the internet, but it is possible to open a connection from your laptop to the newly started pod using port-forwarding capability of kubectl.

```sh
export POD_NAME=$(kubectl get pods --namespace ibu -l "app.kubernetes.io/name=ibu-backend,app.kubernetes.io/instance=ibu-backend" -o jsonpath="{.items[0].metadata.name}")
export CONTAINER_PORT=$(kubectl get pod --namespace ibu $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
kubectl --namespace ibu port-forward $POD_NAME 8000:$CONTAINER_PORT
```

The ibu-backend API is accessible on localhost: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), verify the access to the prompts, agents, and tools using a second terminal or using the Web Browser.

```sh
curl -X 'GET'  'http://127.0.0.1:8000/api/v1/a/prompts/' -H 'accept: application/json'
# 
curl -X 'GET'  'http://127.0.0.1:8000/api/v1/a/agents/' -H 'accept: application/json'
```

Stop the tunneling using ctrl-C.

### Some configuration explanations

The API Keys to access the LLM used are defined in a secret named 

## Deploy OWL Frontend 


A helm chart is defined in the `owl-frontend` folder

```sh
make deploy_owl_frontend
# Or if already deployed
make upgrade_owl_frontend
```

* Get access to the front end using localhost and port-forward capability:

```sh
export POD_NAME=$(kubectl get pods --namespace ibu -l "app.kubernetes.io/name=owl-frontend,app.kubernetes.io/instance=owl-frontend" -o jsonpath="{.items[0].metadata.name}")
export CONTAINER_PORT=$(kubectl get pod --namespace ibu $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
kubectl --namespace ibu port-forward $POD_NAME 3000:$CONTAINER_PORT
```

The url is [http://127.0.0.1:3000/](http://127.0.0.1:3000/),

## Deploying IBM ODM dev image

The instructions are in this IBM's repository: [IBM-ODM-Kubernetes](https://github.com/DecisionsDev/odm-docker-kubernetes), which can be summarized as:

* Add IBM Help chars repository

```sh
helm repo add ibmcharts https://raw.githubusercontent.com/IBM/charts/master/repo/ibm-helm
helm repo update
```

* Check your access to the ODM chart

```sh
helm search repo ibm-odm-prod
```

* Use the make target to deploy ODM

```sh
make deploy_odm_dev
```

The development image does not use a remote database backend, like the postgresql database cluster. The "internal" database is persisted on the local kubernetes worker node file system. So we may need to deploy the ComplainHandling RuleApp to the decision server. 

To access the decision server console, we can also do a port forward on ODM port number:

```sh
export POD_NAME=$(kubectl get pods --namespace ibu -l "app.kubernetes.io/name=ibm-odm-dev,app.kubernetes.io/instance=ibm-odm-dev" -o jsonpath="{.items[0].metadata.name}")
export CONTAINER_PORT=$(kubectl get pod --namespace ibu $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
kubectl --namespace ibu port-forward $POD_NAME 9060:$CONTAINER_PORT
```

or use make as: `make connect_to_odm`

To get the password of the resAdmin, decode the secrets: 

```sh
kubectl get secret ibu-odm-dev-odm-secret -o jsonpath='{.data.users-password}' | base64 --decode
# or
make odm_user_pwd
```

* Upload the ruleapp from deployment/k8s/RuleApp-archive
* Add the resources for the xom jar file (datamgt/code/xom-insurance-pc-claims/target/xom-insurance-pc-claims-1.0.0-SNAPSHOT.jar) and attach the resource to the `ComplaintHandling` library

## Exposing the Owl Frontend to the internet

As we do not have control to the security policies of the VPC managed by our system admin, we will use their loadbalancer and the istio routing via VirtualService.

To read more about this kind of routing [see this article](https://istio.io/latest/docs/reference/config/networking/virtual-service/).

The system administrator shared the following important information:

* 
