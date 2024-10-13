To run the `docker compose` commands, you have to explicitly choose one of the two files:
- `docker-compose-dev.yaml`: Uses the generic `athenadecisionsystems/athena-owl-backend` image that loads the code dynamically. This reduces the "change code-test" cycle to below 1 minute and is typically for development activities
- `docker-compose-pack.yaml`: Uses the specific packaged `athenadecisionsystems/ibu-insurance` image. This is typically for cloud deployment activities

To refer to a specific file, use the `-f` option, for example: `docker compose -f .\docker-compose-dev.yaml up -d`