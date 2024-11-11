# Kubernetes Deployment for the demonstration

This document centralizes materials to deploy OWL demonstrations and solutions to a Kubernetes platform. As target cluster we will use Scaleway cloud provider kubernetes services. As a first solution, we will use IBU Insurance demo.

The goal is to deploy all the components in one command:

```sh
make deploy_all
```

but is is important to understand how each component are deployed as there are some dependencies:

* Deploy a Postgresql cluster using Postgres kubernetes operator: [Cloudnative PG](https://github.com/cloudnative-pg/cloudnative-pg). 
* Deploy the Data Manager service for the IBU Insurance demo.
* Deploy KeyCloack

Most of the commands are added to a unique Makefile to simplify the deployment of a solution.

## A Kubernetes Playground

If you know nothing about Kubernetes, maybe start with [this official tutorial](https://kubernetes.io/docs/tutorials/), RedHat has also very [good content starting with](https://developers.redhat.com/products/openshift/overview). Also for ODM experts, it is mandatory to read [this git repo: Deploying IBM Operational Decision Manager on a Certified Kubernetes Cluster.](https://github.com/DecisionsDev/odm-docker-kubernetes)

We recommend using a local kubernetes with Minikube (See [installation guide](https://kubernetes.io/docs/tasks/tools/install-minikube)) or with [KinD](https://kind.sigs.k8s.io/docs/user/quick-start).

### Tools needed

The following CLI are needed:

* helm [See installation instructions.](https://helm.sh/docs/intro/quickstart/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* The `.env` file with the different environment variables used in the OWL Backend with API Key secrets.

### Access to Scaleway

To access Scaleway, there is a kubernetes cluster already created by a system administrator. Be sure to get the security tokens and the access username within the file named: 
`athena-demo_ibu_kubeconfig`, which is a kubeconfig specification manifest used to access the athena-demo cluster with write access on `ibu` namespace. Normally this file can be saved under `$HOME/.kube` folder. (If you have an existing `.kube/config` file to define existing Kubernetes contexts, then you may want to merge the  `athena-demo_ibu_kubeconfig` content into this `.kube/config` file, and then set the current context to `athena-demo`). 

Use this command to specify the kubectl context to use, so that all commands done with kubectl will go to the Scaleway cluster.

```sh
export KUBECONFIG=~/.kube/athena-demo_ibu_kubeconfig
```

* Verify you can access the Scaleway cluster:

* List the nodes within Kubernetes

```sh
$ kubectl get nodes 
NAME                                             STATUS   ROLES    AGE     VERSION
scw-athena-demo-infra-4c7f37b95e7a40d7b78375fb   Ready    <none>   4h55m   v1.30.2
scw-athena-demo-runners-a1fb1bcfe50647eabf642c   Ready    <none>   122m    v1.30.2
```

* Verify the namespaces

```
kubectl get  ns
```

## Postgres deployment

Even if for production it may be relevant to consider using a managed services to deploy postgresql, like AWS RDS, it is also possible to deploy Postgres on k8s using Operator. Operator automate the deployment and keep it overtime according to the specification defined in the Customer Resource Definition.

CloudNativePG has been designed by Postgres experts with Kubernetes administrators in mind. We recommend reading [this introduction](https://github.com/cloudnative-pg/cloudnative-pg), you will find some good articles about the value of this operator.

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

There are multiple options, we select the deployment within a single kubernetes cluster using asynchronous streaming replication to manage multiple hot standby postgres server replicas. This will create 3 services for applications:

* -rw: applications connect only to the primary instance of the cluster
* -ro: applications connect only to hot standby replicas for read-only-workloads
* -r: applications connect to any of the instances for read-only workloads 

(Read more from [this article](https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/architecture.md#postgresql-architecture))

For application like the DataManager will connect to the Postgres rw service via dns, using service.namespace names. The PostgreSQL operator generates two basic-auth type secrets for every PostgreSQL cluster it deploys:

1. [cluster name]-app 
1. [cluster name]-superuser

We uses the `-app` secrets to access to the DB.

* Deploy a Postgresql cluster with one active node and 2 backup nodes

[Good article](https://www.cncf.io/blog/2023/09/29/recommended-architectures-for-postgresql-in-kubernetes/) to get best practices and design considerations for PostgreSQL deployments in Kubernetes.

See the CRD for a 3-node PostgreSQL cluster, in the `postgresql` folder. The `make` target to deploy the cluster is:

```sh
make deploy_postgresql
```

* We can verify the 3 pods are started with:

```sh
kubectl get pods -n ibu
```

* The 3 services 

```sh
kubectl get svc -n ibu
```

* Get a deeper review of the cluster deployment:

```sh
kubectl describe cluster -n ibu
```

* The secrets:

```sh
kubectl get secrets -n ibu
# Verify the JDBC URI
kubectl get secret athena-pg-cluster-app -o jsonpath='{.data.jdbc-uri}' | base64 --decode
```

The Database servers are exposed only internally within the Kubernetes cluster. The service type is ClusterIP.

## Deploy the DataManager

A helm chart is defined in the `ibu-data-mgr` folder. This microservice is a backend and should not be exposed to the internet, so it is also deployed with ClusterIP service.

To access the Postgresql cluster in the same namespace it needs the admin user name, its password and the jdbc connection URL. Those were defined during the Postgresql cluster deployment. The helm chart is under ibu-data-mgr folder and is a standard chart. The deployment has environment variables defined to use the postgresql secrets.

To deploy do the following command:

```sh
# First time to deploy
make  deploy_data_mgr
# Any changes to the values.yaml or deployment.yaml can be propagated to the running pod via
make upgrade_data_mgr
```

It should display a note explaining how to quickly test the access to the service using port forwarding.

```sh
export POD_NAME=$(kubectl get pods --namespace ibu -l "app.kubernetes.io/name=ibu-data-mgr,app.kubernetes.io/instance=ibu-data-mgr" -o jsonpath="{.items[0].metadata.name}")
export CONTAINER_PORT=$(kubectl get pod --namespace ibu $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
kubectl --namespace ibu port-forward $POD_NAME 8080:$CONTAINER_PORT
```

### Troubleshooting

If the pod is in state `CreateContainerConfigError` use the pod description to get the error: ` kubectl describe pod ibu-data-mgr`. 

## Deploy IBU backend

A helm chart is defined in the `ibu-backend` folder

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

```sh
export POD_NAME=$(kubectl get pods --namespace ibu -l "app.kubernetes.io/name=ibu-data-mgr,app.kubernetes.io/instance=ibu-data-mgr" -o jsonpath="{.items[0].metadata.name}")
export CONTAINER_PORT=$(kubectl get pod --namespace ibu $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
kubectl --namespace ibu port-forward $POD_NAME 8000:$CONTAINER_PORT
```

## Deploy OWL Frontend 


A helm chart is defined in the `owl-frontend` folder

```sh
make deploy_owl_frontend
# Or if already deployed
make upgrade_owl_frontend
```

* Get access locally to the front end

```sh
export POD_NAME=$(kubectl get pods --namespace ibu -l "app.kubernetes.io/name=owl-frontend,app.kubernetes.io/instance=owl-frontend" -o jsonpath="{.items[0].metadata.name}")
export CONTAINER_PORT=$(kubectl get pod --namespace ibu $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
kubectl --namespace ibu port-forward $POD_NAME 3000:$CONTAINER_PORT
```

