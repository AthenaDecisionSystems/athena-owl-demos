# IBU Insurance Demonstration OWL Backend

This folder includes the specific for the demonstration of IBU insurance demonstration using tools and configuration to adapt the owl-agent-backend.

05/22 integrate owl-agent-backend
06/06: integrate new document management into ibu_backend component


* [Optional] The glossary and the prompts may be initiated with the following command, under the ibu_backend/bootstrap folder. As of now those files are committed in github so no need to be run. This is for future updates.

    ```sh
    # under ibu_backend/bootstrap
    python ibu_setup.py
    ```

    This will create two json files under the config folder: `glossary.json` and `prompts.json`.


## IBU Development practices

The IBU insurance backend specific code is under `src/ibu`. 

As most of the agent work is about integration, so there is a docker file for integration tests to start the external components like (ODM RES, Data Manager, Postgresql). If you do not have docker desktop tool, you can use minikube and deploy those components.

```sh
 docker-compose -f tests/data-backend-dc.yaml up -d
```

To start the backend in development mode, where code update is propagated, run:

```sh
# under src
./start_backend.sh
```

As the backend uses Fast API there is a swagger UI for the backend:

[http://localhost:8000/docs](http://localhost:8000/docs)


* The swagger for the client and claim backend is at : [http://localhost:8080/q/swagger-ui](http://localhost:8080/q/swagger-ui).

## Build

Be sure to have docker engine to build image.

Use docker build to package the ibu-backend image.

```sh
# under ibu_backend folder
./build/buildImage.sh
```


## Integration tests

All the integration tests are in tests/it folder. To run them use:

```sh
# all tests executed
pytest -s tests/it/
# a specific tests
pytest -s tests/it/test_app_api.py
```

The configuration file used by the tests is `tests/it/config/config.yaml`

---------------------------------------- STOPPED HERE -> OLD DOC -----------------------



If you run with minikube as a docker engine, be sure to set the docker env:

* Set docker env

```sh
eval  $(minikube docker-env)
```

#### Running the more complete solution

```sh
export OPENAI_API_KEY=<YOUR_API_KEY>
docker-compose up -d
```

* Data Manager for Claim and Client: [http://localhost:8080/](http://localhost:8080/)
* Decision Service: [http://localhost:9060/](http://localhost:9060/)  user resAdmin
* PgAdmin to manage postgresql: [http://localhost:5050/](http://localhost:5050/) user admin@admin.com, password: root and then the connection defined for a local server, name is postgres, user: postgres and password: p0stgrespwd
* Front end for the demo:  [http://localhost:8501/](http://localhost:8501/)


### Run with Minikube

If you are using [Minikube](https://minikube.sigs.k8s.io/docs/start/), be sure to have `kubectl` installed: `alias k="minikube kubectl"` and configure the docker engine, so it is possible to build the images:

```sh
eval  $(minikube docker-env)
```

* Build the docker images with `buildAll.sh`, then make them referenced in minikube (not sure it is needed !)

```sh
minikube image load  athena/backend:latest
minikube image load  athena/frontend:latest
```

* Ensure kubectl works:

```sh
k version
k get nodes
```

* Create a namespace for the app: `kubectl -f deployment/k8s/namespace.yaml`

* Create a secret from the .env file which includes the different LLM API_KEYs:

```sh
kubectl create secret generic  backend-secrets --from-env-file=.env -n athena
# verify - the keys are base64 encrypted
kubectl describe secrets backend-secrets -n athena
```

This secret is used in the deployment to load environment variables for the backend.

* Get minikube IP address: 

```sh
export MINIKUB_IP=$(minikube ip)
```

* Deploy the backend

```sh
kubectl create -f deployment/k8s/backend/deployment.yaml
```

If you need to redeploy the backend

```sh
kubectl rollout restart -f deployment/k8s/backend/deployment.yaml
```

* Deploy the frontend app

```sh
kubectl create -f deployment/k8s/frontend/deployment.yaml
```

* Get the Front End URL by getting the NodePort port number of the service

```sh
kubectl describe svc frontend-service
```

* Deploy ingress
* Undeploy

```sh
kubectl delete -f deployment/k8s/backend/deployment.yaml
kubectl delete -f deployment/k8s/frontend/deployment.yaml
```

There is a script to do that under deployment/k8s: `deleteAll.sh`

