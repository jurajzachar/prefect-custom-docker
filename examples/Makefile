# Variables
REGISTRY = myregistry:5000/mygroup
WORK_POOL = docker-pool
PREFECT_API_URL = http://my-prefect-server:4200/api

# Deploy prefect flow by spinning up a Docker container with 'prefect-custom-docker'
deploy_prefect:
	docker run --rm \
		-e PREFECT_API_URL=$(PREFECT_API_URL) \
		-v .:/app/deploy \
		$(REGISTRY)/prefect-custom-docker:latest \
		bash -c "\
			prefect --no-prompt deploy \
				--concurrency-limit 1 \
				--pool $(WORK_POOL) \
				--collision-strategy 'CANCEL_NEW' \
				--prefect-file ./deploy/prefect.yaml \
		"
	@echo "✅ MyApp ETL flow deployed to Prefect server at $(PREFECT_API_URL)"