# IBU-Insurance demonstration

* 04/20/24: Current demo supports OpenAI.
* 06/06/24: Tune docker compose and configuration for ibu_backend component
* 09/28/2024: The repository includes git action workflows to build the backend and the datamgr docker images and pushed to dockerhub. 
Docker compose to run locally uses new images and simplerconfiguration. Added K8S deployments.

[See the documentation in mkdocs format]()

See the IBU backend readme.md for development activities and how to build the image used in the demonstration. The docker compose file to run locally is under `deployment/local`.

## Prerequisites

For end-to-end testing and demonstration purpose, it is better to have the docker engine with the docker compose cli installed. If you are not able to use Docker Desktop, you can use minikube and then specify the docker engine (see minikube section below).

Be sure to have the docker engine running to build the images and be able to run docker-compose. Building the images are not mandatory. The last updated images are in Docker Hub.

## Run in one command

* Get the LLM KEYs like OpenAI key or WatsonX keys and put them in the `.env` file using `#.env#` file template.
* Start with docker compose:

```sh
# under dpeloyment/local
docker compose up -d
```

The OWL User interface is at [http://localhost:3000](http://localhost:3000).

The demonstration script is in [Get Started](https://athenadecisionsystems.github.io/athena-docs/Get%20started/1-Run%20a%20demo/)

* To validate the application runs as expected there is a end to end on regression test python script under the `e2e` folder:

```sh
python --version
> Python 3.11.9
python non_regression_tests.py
```


## Kubernetes deployment

### Scaleway kubernetes

! TO BE COMPLETED

* Get the Kubeconfig with cluster reference and secrets from your administrator and set it as context in the $USER_HOME/.kube/config file.

The Kubernetes environment has a namespace called **ibu** to deploy the demonstrations. For the IBU insurance, we need to deploy the data manager microservice to access insurance data, a postgrsql srever, the ODM decision service, the frontend and the custom ibu_backend.

* Use `make` CLI with the Makefile under the deployment folder, the following targets can  be used

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


### Using Minikube

! TO BE COMPLETED

* Install [Minikube](https://minikube.sigs.k8s.io/docs/start/)
* Be sure to have `kubectl` installed: `alias k="minikube kubectl"` and configure the docker engine, so it is possible to build the images:

```sh
eval  $(minikube docker-env)
```

* Ensure kubectl and minikube work:

```sh
kubectl version
kubectl get nodes
kubectl get pod -A
```


* Get minikube IP address: 

```sh
export MINIKUB_IP=$(minikube ip)
```


## Development activities

In case you want to do some development tasks. The IBU insurance backend specific code is under `ibu_backend/src/ibu`.

Most of the agent development work is around integration with external databases, decision service, and so on, so there is a docker file for integration tests to start the external components like (ODM RES, Data Manager, Postgresql). If you do not have the docker desktop tool, you can use minikube and deploy those components.

```sh

 docker-compose -f tests/docker-compose.yaml up -d
```

The backend uses [Fast API](https://fastapi.tiangolo.com/) which means you can access an OpenAPI (Swagger) UI to understand all the available endpoints:

[http://localhost:8002/docs](http://localhost:8002/docs)


The swagger for the client and claim data repository is at : [http://localhost:8080/q/swagger-ui](http://localhost:8080/q/swagger-ui). This code is a quarkus app with Posgresql to persist sample data. The source code of this Java app is in [IBU-insurance-demo/datamgt/code/apis-datamgt-insurance-pc-claims](./datamgt/code/apis-datamgt-insurance-pc-claims). 
If really needed, you may build this app, by using the buildImage.sh script in the `datamgt/build` folder. This image is built on Pull Request on the main repository.

```sh
# under IBU-insurance-demo/datamgt/
./build/buildImage.sh
```

### IBU Backend development

The core of the development may be around the python code in ibu_agent/src. 

One of the main principle of the owl-agent backend is that the core of the server runs as a container and the custom code, with the configuration, are mounted inside the container. So the docker compose under the tests folder starts this container:

```yaml
ibu-backend:
    hostname: ibu-backend
    image: athenadecisionsystems/athena-owl-backend:1.0.0
    container_name: ibu-backend
    ports:
      - 8002:8000
    environment:
      CONFIG_FILE: /app/config/config.yaml
    env_file:
      - .env
    volumes:
      - ../src/config:/app/config
      - ../../.env:/app/.env
      - ./data/:/app/data
      - ../src/ibu:/app/ibu
```

The anchor inside the container is the `/app` folder with the following subfolders:

```
athena                  --> the code of the core backend
config                  --> the configuration for the demonstration
data                    --> the content for vector store collection, and uploaded files
ibu                     --> the custom code dor an agent or the integration
```

When the backend is running with docker, any new change to the code could be integrated by restarting the iu-backend container:

```sh
docker stop ibu-backend
docker rm ibu-backend
docker compose up -d
```

### Run unit tests

The unit tests do no need to have all the containers of the solution running. They test at the service level.

Before running any tests, you need to set the PYTHONPATH to access the source code for owl agent. This means you need to clode the core code, if not done already

```sh
# in a Code folder for example
git clone https://github.com/AthenaDecisionSystems/athena-owl-core
ls
> athena-owl-core
> athena-owl-demos
cd athena-owl-demos/IBU-insurance-demo/ibu_backend
source setpython.sh
```


### Run locally
```sh
cd athena-owl-demos/IBU-insurance-demo/ibu_backend
source setpython.sh
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt
cd src
./start_backend.sh
```


```sh
# Run all tests
pytest -s tests/ut
# Run a specific test, specially the ibu-agent code
pytest -s tests/ut/test_ibu_agents.py
```

#### Build the image

Drugin development there is no need to build the demo image. It may be relevant to package it as a bundled image containing the custom demo code and the core code. For that use the script to package the ibu-backend image.

```sh
# in ibu_backend folder
./build/buildImage.sh
```


### Integration tests

All the integration tests are in the `tests/it` folder. To run them use:

```sh
# Execute all tests
pytest -s tests/it/
# run a specific test
pytest -s tests/it/test_app_api.py # or other test file
```

The configuration file used by the tests is `tests/it/config/config.yaml`
