# Makefile
REGISTRY = calbuco:5000/thorium
IMAGE = prefect-custom-docker
GIT_COMMIT := $(shell git rev-parse --short HEAD)
WORK_POOL = docker-pool

.PHONY: build test docker_push

build:
	poetry self add poetry-plugin-export
	poetry export --without-hashes --output requirements.txt
	docker build -t $(REGISTRY)/$(IMAGE):latest .
	docker tag $(REGISTRY)/$(IMAGE):latest $(REGISTRY)/$(IMAGE):$(GIT_COMMIT)

test:
	export PYENV_ROOT=$$HOME/.pyenv; \
	export PATH=$$PYENV_ROOT/bin:$$PYENV_ROOT/shims:$$PATH; \
	eval "$$($$PYENV_ROOT/bin/pyenv init -)"; \
	poetry env use 3.13; \
	poetry install; \
	poetry run pytest

docker_push:
	docker push $(REGISTRY)/$(IMAGE):$(GIT_COMMIT)
	docker push $(REGISTRY)/$(IMAGE):latest