#!/bin/bash

# Define the required environment variables
REQUIRED_ENV_VARS=("IBM_WATSONX_APIKEY" "IBM_WATSON_PROJECT_ID" "IBM_WATSONX_URL" "WATSONX_APIKEY" "WATSONX_PROJECT_ID" "WATSONX_URL" "OPENAI_API_KEY" "LANGCHAIN_API_KEY" "LANGCHAIN_ENDPOINT" "TAVILY_API_KEY" "OWL_CLIENTS")

# Function to check if the .env file exists and has the required environment variables
check_env_file() {
    if [ ! -f ./.env ]; then
        echo ".env file not found!"
        exit 1
    fi

    for var in "${REQUIRED_ENV_VARS[@]}"; do
        value=$(grep -v '^#' .env | grep -w "$var" | cut -d '=' -f2-)
        if [ -z "$value" ]; then
            echo "Environment variable $var is not set or is empty in the .env file!"
            exit 1
        fi
    done
}

# Check if the .env file has the necessary environment variables
check_env_file

# Default mode is packaged
MODE="packaged"

# Check for the -dev option
if [ "$1" == "-dev" ]; then
    MODE="dev"
fi

# Execute the correct docker-compose command
if [ "$MODE" == "dev" ]; then
    echo "Starting in development mode..."
    docker compose -f ./docker-compose-dev.yaml up -d
else
    echo "Starting in packaged mode..."
    docker compose -f ./docker-compose-pack.yaml up -d
fi
