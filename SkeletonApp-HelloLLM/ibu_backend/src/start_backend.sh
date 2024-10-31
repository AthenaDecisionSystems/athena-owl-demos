#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to create a directory if it does not already exist
create_directory_if_not_exists() {
    local dir_path=$1
    if [ ! -d "$dir_path" ]; then
        echo "Creating directory: $dir_path"
        mkdir -p "$dir_path"
    else
        echo "Directory already exists: $dir_path"
    fi
}

# Create datastore folder, file_uploads folder, and vector_store_db folder if they don't exist
create_directory_if_not_exists "../../datastore"
create_directory_if_not_exists "../../datastore/file_uploads"
create_directory_if_not_exists "../../datastore/vector_store_db"

# Detect the absolute paths dynamically
OWL_AGENT_BACKEND_SRC=$(realpath "$(pwd)/../../../../athena-owl-core/owl-agent-backend/src")
IBU_BACKEND_SRC=$(realpath "$(pwd)")

# Uncomment the following lines if you want to define a virtual env at the app level and active it automatically
# Activate the virtual environment (ensure the .venv exists and is valid)
# if [ -f ".venv/bin/activate" ]; then
#     echo "Activating virtual environment"
#     source .venv/bin/activate
# else
#     echo "Virtual environment not found. Please ensure .venv is set up correctly."
#     exit 1
# fi

# Export the PYTHONPATH
export PYTHONPATH="${OWL_AGENT_BACKEND_SRC}:${IBU_BACKEND_SRC}"
echo "PYTHONPATH set to: $PYTHONPATH"

# Set configuration environment variables
export CONFIG_FILE="./config/config_dev_outside_docker.yaml"
export OWL_CLIENTS="[http://localhost:3000]"

# Print environment variables for verification
echo "CONFIG_FILE set to: $CONFIG_FILE"
echo "OWL_CLIENTS set to: $OWL_CLIENTS"

# Run the backend server
echo "Starting Uvicorn server..."
uvicorn athena.main:app --host 0.0.0.0 --port 8002 --reload