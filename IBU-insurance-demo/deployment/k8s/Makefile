.PHONY: create_ns e2e_owl_backend
# Setting global variables
DEV_NS ?= ibu
IBU_BACKEND ?= ibu-backend
OWL_FRONTEND ?= owl-frontend
IBU_DATAMGR ?= ibu-data-mgr
IBU_DB ?= ibu-db-postgresql

# ------------------------
# Reusable functions
# -----------------------
ensure_ns = \
	@kubectl get ns $1 >/dev/null 2>&1; \
	if [ $$? -ne 0 ]; then \
			kubectl create ns $1; \
	else \
			echo "$1 exists";\
	fi

# -------------------------------------------------------
# Entry points for aggregated targets
# -------------------------------------------------------
prepare: create_ns create_secret_from_env deploy_postgres_operator deploy_postgresql 

deploy_all: prepare  deploy_data_mgr deploy_ibu_backend deploy_odm_dev deploy_owl_frontend

# ------------------
# one time settings
# ------------------

create_ns:
	$(call ensure_ns, $(DEV_NC))

create_secret_from_env:
	@kubectl create secret generic ibu-dotenv --from-env-file=../local/.env -n $(DEV_NS)

clean:
	@helm delete $(IBU_DATAMGR)
	@helm delete $(IBU_DB)
	@helm delete $(IBU_BACKEND)
	@helm delete $(OWL_FRONTEND)
	@helm delete ibu-odm-dev
	# -- add undeploy postgres ?

set_k8s_context:
	@kubectl config  --kubeconfig=$HOME/.kube/config  use-context athena-demo

# ----------------------------- POSTGRESQL -------------
deploy_postgres_operator:
	@kubectl apply --server-side -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.24/releases/cnpg-1.24.1.yaml


deploy_postgresql:
	@kubectl apply -f postgresql/pg-cluster.yaml  -n $(DEV_NS)


get_postgresql_pwd:
	@kubectl get secret --namespace  $(DEV_NS) $(IBU_DB) -o jsonpath="{.data.postgres-password}" | base64 -d 


# Application specifics
# ------------------------------ DataManager microservice -------------------------
deploy_data_mgr:
	@helm install $(IBU_DATAMGR) $(IBU_DATAMGR) -n $(DEV_NS)

upgrade_data_mgr:
	@helm upgrade $(IBU_DATAMGR) $(IBU_DATAMGR)  -n $(DEV_NS)

connect_to_data_mgr:
	@POD_NAME=$$(kubectl get pods --namespace $(DEV_NS) -l "app.kubernetes.io/name=ibu-data-mgr,app.kubernetes.io/instance=ibu-data-mgr" -o jsonpath="{.items[0].metadata.name}"); \
	CONTAINER_PORT=$$(kubectl get pod --namespace $(DEV_NS) $$POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}"); \
	kubectl --namespace $(DEV_NS) port-forward $$POD_NAME 8080:$$CONTAINER_PORT

# ------------------------ IBU / Owl backend ----------------------------
deploy_ibu_backend:
	@helm install $(IBU_BACKEND) $(IBU_BACKEND) -n $(DEV_NS)

upgrade_ibu_backend:
	@helm upgrade $(IBU_BACKEND) $(IBU_BACKEND)  -n $(DEV_NS)

delete_ibu_backend:
	@helm delete $(IBU_BACKEND) -n $(DEV_NS)

connect_to_backend:
	@POD_NAME=$$(kubectl get pods --namespace $(DEV_NS) -l "app.kubernetes.io/name=ibu-backend,app.kubernetes.io/instance=ibu-backend" -o jsonpath="{.items[0].metadata.name}"); \
	CONTAINER_PORT=$$(kubectl get pod --namespace $(DEV_NS) $$POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}"); \
	kubectl --namespace $(DEV_NS) port-forward $$POD_NAME 8000:$$CONTAINER_PORT

# ----------------------------------OWL FRONTEND ---------------------------------
deploy_owl_frontend:
	@helm install $(OWL_FRONTEND) $(OWL_FRONTEND) -n $(DEV_NS)

upgrade_owl_frontend:
	@helm upgrade $(OWL_FRONTEND) $(OWL_FRONTEND)  -n $(DEV_NS)

connect_to_frontend:
	POD_NAME=$$(kubectl get pods --namespace $(DEV_NS) -l "app.kubernetes.io/name=owl-frontend,app.kubernetes.io/instance=owl-frontend" -o jsonpath="{.items[0].metadata.name}"); \
	echo $$POD_NAME; \
	CONTAINER_PORT=$$(kubectl get pod --namespace $(DEV_NS) $$POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}");  echo $$CONTAINER_PORT;\
	kubectl --namespace $(DEV_NS) port-forward $$POD_NAME 3000:$$CONTAINER_PORT

# -------------------------- ODM --------------------------------------
deploy_odm_dev:
	@helm install ibu-odm-dev --set license=accept --set usersPassword=iburesAdmin ibm-helm/ibm-odm-dev -n $(DEV_NS)

info_odm_dev:
	@helm status ibu-odm-dev
	@helm get values ibu-odm-dev
	@helm get hooks ibu-odm-dev

# --- the following will not work as there is no authorization rules in the network policies define to get inbound traffic to the VPC, use next target
where_is_odm:
	@NODE_PORT=$$(kubectl get --namespace ibu -o jsonpath="{.spec.ports[0].nodePort}" services ibu-odm-dev-ibm-odm-dev); \
 	NODE_IP=$(kubectl get nodes --namespace ibu -o jsonpath="{.items[0].status.addresses[0].address}"); \
	echo http://$$NODE_IP:$$NODE_PORT/res

connect_to_odm:
	@POD_NAME=$$(kubectl get pods --namespace ibu -l "app.kubernetes.io/name=ibm-odm-dev,app.kubernetes.io/instance=ibm-odm-dev" -o jsonpath="{.items[0].metadata.name}"); \
	CONTAINER_PORT=$(kubectl get pod --namespace ibu $$POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}") \
	kubectl --namespace  $(DEV_NS) port-forward $$POD_NAME 9060:$$CONTAINER_PORT

odm_user_pwd:
	kubectl get secret ibu-odm-dev-odm-secret -o jsonpath='{.data.users-password}' | base64 --decode

list_odm_releases:
	@helm repo list
	@helm repo update
	@helm search repo ibm-odm-prod -l






# -------------------------- GET Some Addresses to validate deployment --------------------------------------

get_pod_port = \
	@PODNAME=$$(kubectl get pods --namespace $(DEV_NS) -l "app.kubernetes.io/name=$1,app.kubernetes.io/instance=$1" -o jsonpath="{.items[0].metadata.name}"); \
	echo $(POD_NAME) \
	@CONTAINER_PORT=$$(kubectl get pod --namespace ibu $(POD_NAME) -o jsonpath="{.spec.containers[0].ports[0].containerPort}") ; \
	echo $(CONTAINER_PORT)

get_ibu_data_mgr_address:
	@echo "Fetching internal address for $(IBU_DATAMGR) in namespace $(DEV_NS)..."
	@POD_NAME=$$(kubectl get pods --namespace $(DEV_NS) -l "app.kubernetes.io/name=ibu-data-mgr,app.kubernetes.io/instance=ibu-data-mgr" -o jsonpath="{.items[0].metadata.name}"); \
	echo $(POD_NAME) \
	@CONTAINER_PORT=$$(kubectl get pod --namespace ibu $(POD_NAME) -o jsonpath="{.spec.containers[0].ports[0].containerPort}") ; \
	if [ -z "$(POD_NAME)" ]; then \
		echo "Error: Unable to retrieve internal address. The service might not have an external IP or hostname."; \
		echo "Current service status:"; \
		kubectl get svc --namespace $(DEV_NS) $(IBU_DATAMGR) -o wide; \
		exit 1; \
	else \
		echo "Visit http://127.0.0.1:8080"; \
		kubectl --namespace $(DEV_NS) port-forward $(POD_NAME) 8080:$(CONTAINER_PORT); \
	fi


get_ibu_backend_address:
	@echo "Fetching external address for $(IBU_BACKEND) in namespace $(DEV_NS)..."
	@ADDRESS=$$(kubectl get svc --namespace $(DEV_NS) $(IBU_BACKEND) -o jsonpath='{.status.loadBalancer.ingress[0].ip}'); \
	if [ -z "$$ADDRESS" ]; then \
		ADDRESS=$$(kubectl get svc --namespace $(DEV_NS) $(IBU_BACKEND) -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'); \
	fi; \
	if [ -z "$(ADDRESS)" ]; then \
		echo "Error: Unable to retrieve external address. The service might not have an external IP or hostname."; \
		echo "Current service status:"; \
		kubectl get svc --namespace $(DEV_NS) $(IBU_BACKEND) -o wide; \
		exit 1; \
	else \
		echo "Service external address: $$ADDRESS"; \
		curl -X GET http://$$ADDRESS:8000/api/v1/version; \
	fi

get_owl_front_address:
	@echo "Fetching external address for $(OWL_FRONTEND) in namespace $(DEV_NS)..."
	@ADDRESS=$$(kubectl get svc --namespace $(DEV_NS) $(OWL_FRONTEND) -o jsonpath='{.status.loadBalancer.ingress[0].ip}'); \
	if [ -z "$(ADDRESS)" ]; then \
		ADDRESS=$$(kubectl get svc --namespace $(DEV_NS) $(OWL_FRONTEND) -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'); \
	fi; \
	if [ -z "$(ADDRESS)" ]; then \
		echo "Error: Unable to retrieve external address. The service might not have an external IP or hostname."; \
		echo "Current service status:"; \
		kubectl get svc --namespace $(DEV_NS) $(OWL_FRONTEND) -o wide; \
		exit 1; \
	else \
		echo "Service external address: $$ADDRESS"; \
		curl -X GET http://$$ADDRESS:3000/; \
	fi


# ------------------------------ KeyCloak -------------------------
deploy_keycloak:
	@kubectl create -f https://raw.githubusercontent.com/keycloak/keycloak-quickstarts/latest/kubernetes/keycloak.yaml