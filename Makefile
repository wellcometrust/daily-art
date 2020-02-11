.DEFAULT_GOAL := all

VIRTUALENV := env
IMAGE := antoniocampello/daily-wellcome-art
VERSION := 2020.2.1

$(VIRTUALENV)/.installed: requirements.txt
	@if [ -d $(VIRTUALENV) ]; then rm -rf $(VIRTUALENV); fi
	@mkdir -p $(VIRTUALENV)
	virtualenv --python python3 $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip3 install -r requirements.txt
	touch $@

.PHONY: virtualenv
virtualenv: $(VIRTUALENV)/.installed

.PHONY: download_data
download_data:
	$(VIRTUALENV)/bin/python3 daily-art/resources/data.py

.PHONY: docker-build
docker-build:
	docker build \
	    -t $(IMAGE):$(VERSION) \
		-t $(IMAGE):latest \
		.

.PHONY: docker-push
docker-push: docker-build
	docker login && \
    docker push $(IMAGE):$(VERSION) && \
    docker push $(IMAGE):latest

.PHONY: all
all: virtualenv download_data
