# IBU Insurance

???+ Info "Version"
    Created 06.2024 . STILL UNDER WORK

The IBU insurance demonstration illustrates the integration with data manager service, a decision service, a vector store and a LLM as shown in the figure below:

![](./diagrams/ibu_ins_sys_ctx.drawio.png){ width=800 }

## Goals

The IBU Insurance agent chatbot helps IBU Insurance’s customer service representatives manage customer complaints about their claims handling. The chatbot is used by the customer service reps when a customer calls or writes with a complaint.

The chatbot should bring consistent responses and actionable decisions, which improves the complain management by more than 27% and improve the quality responses by 35% while reducing the cost by around 60%. 


[![alt text](https://img.youtube.com/vi/fGEU_obHM5M/0.jpg)](https://www.youtube.com/watch?v=fGEU_obHM5M){ width=600 }

[Link to video](https://www.youtube.com/watch?v=fGEU_obHM5M)


## Insurance context

In most insurance organization we may find the following roles Involved in Complaint Handling process:

![](./images/insurance/complaint-stakeholders.PNG)

The AI assistant will help the contact center agents.

## Build for demonstration

For development purpose build the DataManager microservice images:

```sh
cd datamgt
./build/buildImage.sh
```

The docker image for the DataManager microservice, the chatbot frontend and for the OWL Backend are available on docker hub.

![](./images/insurance/dock-hub-images.PNG)

## Run locally

To start all the components of the solution like the owl_backend, the owl_frontend, the data manager, postgresql database, and the ODM decision service, use the docker compose file locally under the `IBU-insurance-demo/deployment/local/` folder. 

```sh
docker-compose up -d 
```

The first time you launch it, it may take some time as it downloads the needed docker images.

Verify that the six containers are running:

```sh
docker ps
```

```
2ecb23b78ad5   jbcodeforce/ibu-insurance-data-mgr:latest  0.0.0.0:8080->8080/tcp, 8443/tcp         datamgr
3988ffd617c6   jbcodeforce/athena-owl-backend:latest      0.0.0.0:8000->8000/tcp                   owl-backend
258460ed25ed   jbcodeforce/athena-owl-frontend:latest      0.0.0.0:3000->80/tcp                   owl-frontend
349f3beb4174   icr.io/cpopen/odm-k8s/odm:8.12             0.0.0.0:9060->9060/tcp, 9080/tcp, 0.0.0.0:9443->9443/tcp, 9453/tcp   decisionsvc
070e124923f7   postgres:latest                            0.0.0.0:5432->5432/tcp                   postgres
86052092cfe7   ghcr.io/chroma-core/chroma:latest          0.0.0.0:8005->8000/tcp                   chroma-db
```

To look at owl-backend logs

```sh
docker logs owl-backend
```

Next see the demonstration script section, or the non-regression tests to automate scenario execution.


## Demonstration Flows


## Architecture

From an high level 



### Query without RAG


### Query with RAG

### Query with RAG and Rule Engine


## Component Definitions

### Define Assistant


### Define Agent

### Define Tools

### Define prompt

### Integration tests

### Non-regression tests

Under the `e2e` folder you can find different tool to support automatic testing

```
python non_regression_tests.py
```
