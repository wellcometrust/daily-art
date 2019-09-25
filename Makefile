.DEFAULT_GOAL := all

VIRTUALENV := env

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

.PHONY: all
all: virtualenv download_data
