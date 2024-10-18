#!/bin/bash

# Default mode is packaged
MODE="packaged"

# Check for the -dev option
if [ "$1" == "-dev" ]; then
    MODE="dev"
fi

# Execute the correct docker-compose command for stopping the demo
if [ "$MODE" == "dev" ]; then
    echo "Stopping development mode..."
    docker compose -f ./docker-compose-dev.yaml down
else
    echo "Stopping packaged mode..."
    docker compose -f ./docker-compose-pack.yaml down
fi
