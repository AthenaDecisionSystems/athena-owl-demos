# IBU-Insurance demonstration

* 04/20/24: Current demo supports OpenAI.
* 06/06/24: Tune docker compose and configuration for ibu_backend component
* 09/24/2024: The repository includes git action workflows to build the backend and the datamgr docker images and pushed to dockerhub. 
Docker compose to run locally uses new images and simpler configuration. Ad K8S deployments

[See the documentation in mkdocs format]()

See the IBU backend readme.md for development activities and how to build the image used in the demonstration. The docker compose file to run locally is under `deployment/local`.

## Component explanation

## Prerequisites

For end-to-end testing and demonstration purpose, it is better to have the docker engine with the docker compose cli installed. If you are not able to use Docker Desktop, you can use minikube and then specify the docker engine (see minikube section below).

Be sure to have the docker engine running to build the image and be able to run docker-compose. 



### Using Minikube

* Install [Minikube](https://minikube.sigs.k8s.io/docs/start/)

 To be continued


## Automatic tests


## Kubernetes deployment

### Scaleway kubernetes

* Get the Kubeconfig with cluster reference and secrets from your administrator and set it as context in the $USER_HOME/.kube/config file.

The Kubernetes environment has a namespace call **ibu** to deploy the demonstrations. For the IBU insurance we will deploy the data manager microservice to access insurance data, and the custom ibu_backend.

* Use make CLI with the Makefile under deployment folder, the following targets can  be used

    * `make set_k8s_context`
    * `make deploy_postgresql` 
    * `make deploy_data_mgr`


PostgreSQL can be accessed via port 5432 on the following DNS names from within your cluster:

    ibu-db-postgresql.ibu.svc.cluster.local - Read/Write connection

To get the password for "postgres" run:

    export POSTGRES_PASSWORD=$(kubectl get secret --namespace ibu ibu-db-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)

To connect to your database run the following command:

    kubectl run ibu-db-postgresql-client --rm --tty -i --restart='Never' --namespace ibu --image docker.io/bitnami/postgresql:16.4.0-debian-12-r9 --env="PGPASSWORD=$POSTGRES_PASSWORD" \
      --command -- psql --host ibu-db-postgresql -U postgres -d postgres -p 5432

 kubectl port-forward --namespace ibu svc/ibu-db-postgresql 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d postgres -p 5432


    1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace ibu -l "app.kubernetes.io/name=ibu-data-mgr,app.kubernetes.io/instance=ibu-data-mgr" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace ibu $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace ibu port-forward $POD_NAME 8080:$CONTAINER_PORT