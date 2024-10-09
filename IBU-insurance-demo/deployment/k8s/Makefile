.PHONY: create_ns e2e_owl_backend
# Setting global variables
DEV_NS ?= ibu
OWL_BACKEND ?= ibu-backend
IBU_BACKEND ?= owl-frontend
IBU_DATAMGR ?= ibu-data-mgr
IBU_DB ?= ibu-db-postgresql
# -------------------------------------------------------
# Entry points
# -------------------------------------------------------
prepare: create_ns create_secret_from_env deploy_postgresql deploy_data_mgr

all: prepare


ensure_ns = \
	@kubectl get ns $1 >/dev/null 2>&1; \
	if [ $$? -ne 0 ]; then \
			kubectl create ns $1; \
	else \
			echo "$1 exists";\
	fi

create_ns:
	$(call ensure_ns, $(DEV_NC))

create_secret_from_env:
	@kubectl create secret generic env --from-file=../../.env -n $(DEV_NS)

deploy_postgresql:
	@helm install $(IBU_DB) oci://registry-1.docker.io/bitnamicharts/postgresql -n $(DEV_NS)

get_postgresql_pwd:
	@kubectl get secret --namespace  $(DEV_NS) $(IBU_DB)-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d 

deploy_data_mgr:
	@helm install $(IBU_DATAMGR) $(IBU_DATAMGR) -n $(DEV_NS)

upgrade_data_mgr:
	@helm upgrade $(IBU_DATAMGR) $(IBU_DATAMGR)  -n $(DEV_NS)

deploy_ibu_backend:
	@helm install $(IBU_BACKEND) $(IBU_BACKEND) -n $(DEV_NS)

upgrade_ibu_backend:
	@helm upgrade $(IBU_BACKEND) $(IBU_BACKEND)  -n $(DEV_NS)

deploy_odm_dev:
	@helm install ibu-odm-dev --set license=accept --set usersPassword=iburesAdmin ibm-helm/ibm-odm-dev -n $(DEV_NS)

info_odm_dev:
	@helm status ibu-odm-dev
	@helm get values ibu-odm-dev
	@helm get hooks ibu-odm-dev

where_is_odm:
	@NODE_PORT=$$(kubectl get --namespace ibu -o jsonpath="{.spec.ports[0].nodePort}" services ibu-odm-dev-ibm-odm-dev); \
 	NODE_IP=$(kubectl get nodes --namespace ibu -o jsonpath="{.items[0].status.addresses[0].address}"); \
	echo http://$$NODE_IP:$$NODE_PORT/res

list_odm_releases:
	@helm repo list
	@helm repo update
	@helm search repo ibm-odm-prod -l


clean:
	@helm delete $(IBU_DATAMGR)
	@helm delete $(IBU_DB)
	@helm delete $(IBU_BACKEND)
	@helm delete ibu-odm-dev

set_k8s_context:
	@kubectl config  --kubeconfig=$HOME/.kube/config  use-context athena-demo

get_ibu_data_mgr_address:
	@echo "Fetching internal address for $(IBU_DATAMGR) in namespace $(DEV_NS)..."
	@POD_NAME=$$(kubectl get pods --namespace $(DEV_NS) $(IBU_DATAMGR) -l "app.kubernetes.io/name=ibu-data-mgr,app.kubernetes.io/instance=ibu-data-mgr" -o jsonpath="{.items[0].metadata.name}"); \
	@CONTAINER_PORT=$$(kubectl get pod --namespace ibu $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}") ; \
	if [ -z "$$POD_NAME" ]; then \
		echo "Error: Unable to retrieve internal address. The service might not have an external IP or hostname."; \
		echo "Current service status:"; \
		kubectl get svc --namespace $(DEV_NS) $(IBU_DATAMGR) -o wide; \
		exit 1; \
	else \
		echo "Visit http://127.0.0.1:8080"; \
		@kubectl --namespace ibu port-forward $POD_NAME 8080:$CONTAINER_PORT; \
	fi


get_ibu_backend_address:
	@echo "Fetching external address for $(IBU_BACKEND) in namespace $(DEV_NS)..."
	@ADDRESS=$$(kubectl get svc --namespace $(DEV_NS) $(IBU_BACKEND) -o jsonpath='{.status.loadBalancer.ingress[0].ip}'); \
	if [ -z "$$ADDRESS" ]; then \
		ADDRESS=$$(kubectl get svc --namespace $(DEV_NS) $(IBU_BACKEND) -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'); \
	fi; \
	if [ -z "$$ADDRESS" ]; then \
		echo "Error: Unable to retrieve external address. The service might not have an external IP or hostname."; \
		echo "Current service status:"; \
		kubectl get svc --namespace $(DEV_NS) $(IBU_BACKEND) -o wide; \
		exit 1; \
	else \
		echo "Service external address: $$ADDRESS"; \
		curl -X GET http://$$ADDRESS:8000/api/v1/version; \
	fi

get_owl_front_address:
	@echo "Fetching external address for $(IBU_BACKEND) in namespace $(DEV_NS)..."
	@ADDRESS=$$(kubectl get svc --namespace $(DEV_NS) $(IBU_BACKEND) -o jsonpath='{.status.loadBalancer.ingress[0].ip}'); \
	if [ -z "$$ADDRESS" ]; then \
		ADDRESS=$$(kubectl get svc --namespace $(DEV_NS) $(IBU_BACKEND) -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'); \
	fi; \
	if [ -z "$$ADDRESS" ]; then \
		echo "Error: Unable to retrieve external address. The service might not have an external IP or hostname."; \
		echo "Current service status:"; \
		kubectl get svc --namespace $(DEV_NS) $(IBU_BACKEND) -o wide; \
		exit 1; \
	else \
		echo "Service external address: $$ADDRESS"; \
		curl -X GET http://$$ADDRESS:3000/; \
	fi