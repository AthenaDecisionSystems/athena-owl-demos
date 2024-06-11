# IBU-Insurance demonstration

* 04/20/24: Current demo supports OpenAI.
* 06/06/24: Tune docker compose and configuration for ibu_backend component

See the IBU backend readme.md for development activities and how to build the image used in the demonstration. The docker compose to run locally is under `deployment\local`.

## Component explanation

## Prerequisites

For end-to-end testing and demonstration purpose, it is better to have the docker engine with the docker compose cli installed. If you are not able to use Docker Desktop, you can use minikube and then specify the docker engine (see minikube section below).

Be sure to have docker engine to build image and be able to run docker-compose. 


## Build for demonstration

* Build the DataManager microservice images:

    ```
    cd datamgt
    ./build/buildImage.sh
    ```

* build the IBU agent backend,

    ```sh
    cd ibu_backend
    ./build/buildImage.sh
    ```


Next see the demonstration script section, or the non-regression tests to automate the validation.

### Using Minikube

* Install [Minikube](https://minikube.sigs.k8s.io/docs/start/)

 To be continued

## Run locally

To start the ibu_agent backend, the data manager, postgresql, and ODM decision service, use the docker compose file locally. 

```sh
docker-compose up -d 
```

Verify that the 4 containers are running:

```sh
docker ps
```

```
2ecb23b78ad5   athena/ibu-insurance-data-mgr     0.0.0.0:8080->8080/tcp, 8443/tcp         datamgr
3988ffd617c6   athena/ibu-backend                0.0.0.0:8000->8000/tcp                   ibu-backend
349f3beb4174   icr.io/cpopen/odm-k8s/odm:8.12    0.0.0.0:9060->9060/tcp, 9080/tcp, 0.0.0.0:9443->9443/tcp, 9453/tcp   decisionsvc
070e124923f7   postgres:latest                   0.0.0.0:5432->5432/tcp                   postgres
```

Look at ibu_backend logs

```sh
docker logs ibu-backend
```


## Automatic tests
