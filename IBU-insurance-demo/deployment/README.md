# Deployment to different platforms

## Running locally using docker

From `deployment/local` folder use docker compose.

```sh
start-demo.sh
```

The URL of the frontend is [http://localhost:3000/](http://localhost:3000/), the backend API [http://localhost:8000/docs](http://localhost:8000/docs), the claim and customer data manager [http://localhost:8080/q/swagger-ui/](http://localhost:8080/q/swagger-ui/) and the rule execution server [http://localhost:9060](http://localhost:9060/). 

To stop everything

```
docker compose -f docker-compose-dev.yaml down
``` 

