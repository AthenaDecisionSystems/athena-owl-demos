# Deployment to different platforms

## Running locally using docker

From deployment/local folder use docker compose.

```sh
docker compose up -d
```

The URL of the frontend is [http://localhost:3000/](http://localhost:3000/), the backend API [http://localhost:8000/docs](http://localhost:8000/docs), the claim and customer data manager [http://localhost:8080/q/swagger-ui/](http://localhost:8080/q/swagger-ui/) and the rule execution server [http://localhost:9060](http://localhost:9060/). 

To stop everything

```
docker compose down
```

## Running local using Minikube and helm charts

This is to validate the deployment and helm charts before deploying to the cloud:

* Start minikube 

```sh
minikube start  --cpus 3
# list addons
minikube addons list 
# Enable ingress if not already enabled
minikube addons enable ingress
# and image registry
minikube addons enable registry -
```

* Move images from local docker to minikube

```
```