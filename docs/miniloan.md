# IBM Miniloan ODM demonstration with Agent


## Goals

The Miniloan application is part of the IBM Operational Decision Management product and [tutorial](https://www.ibm.com/docs/en/odm/8.12.0?topic=rules-tutorials).

## Architecture

At the high level the architecture of this solution looks like in the figure below:

![](./diagrams/hl-arch.drawio.png)


## Demonstration Flows

1. Start the docker compose with all the components of the architecture.

    ```sh
    cd IBM-MiniLoan-demo/deployment/local/
    docker compose up -d
    ```

    The backend APIs is available at the following URL [http://localhost:8000/docs](http://localhost:8000/docs).

1. 

## Agentic with Rule Engine

This section explains the code approach to use Agent for tool calling.

* diagram
* tool definition
* tool factory

## Development around the demonstration

In case you need to work on the current demonstration, and run some of the test cases, this section addresses what needs to be done to run on you local laptop with Docker engine.

### Unit tests

* Define the PYTHONPATH so the core module can be accessed in the unit tests

    ```sh
     export PYTHONPATH=$WHERE_YOUR_CODE_IS/athena-owl-core/owl-agent-backend/src
    ```