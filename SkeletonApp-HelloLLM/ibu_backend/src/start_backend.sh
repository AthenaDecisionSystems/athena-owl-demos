export CONFIG_FILE=./config/config_dev_outside_docker.yaml
export OWL_CLIENTS=[http://localhost:3000]

uvicorn athena.main:app --host 0.0.0.0 --port 8002 --reload 