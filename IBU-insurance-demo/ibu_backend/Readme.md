# IBU Insurance Demonstration OWL Backend

This readme is deprecated, the new content is in [IBU-insurance-demo folder](../Readme.md)



## OLD notes to revisite or migrate in product doc

[Optional] The glossary and the prompts may be initiated with the following command, under the `ibu_backend/bootstrap` folder. These files are committed in github so no need to be run. This is for future updates.

```sh
# in the folder ibu_backend/bootstrap
python ibu_setup.py
```

This will create two json files under the config folder: `glossary.json` and `prompts.json`.



---------------------------------------- STOPPED HERE -> OLD DOC -----------------------


### Run with Minikube

\
* Build the docker images with `buildAll.sh`, then make them referenced in minikube (not sure it is needed !)

```sh
minikube image load  athena/backend:latest
minikube image load  athena/frontend:latest
```



* Create a namespace for the app: `kubectl -f deployment/k8s/namespace.yaml`

* Create a secret from the .env file which includes the different LLM API_KEYs:

```sh
kubectl create secret generic  backend-secrets --from-env-file=.env -n athena
# verify - the keys are base64 encrypted
kubectl describe secrets backend-secrets -n athena
```

This secret is used in the deployment to load environment variables for the backend.


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

