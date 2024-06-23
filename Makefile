VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
FLASK = $(VENV_DIR)/bin/flask
TESTS_DIR = tests
REQUIREMENTS_FILE = requirements.txt

.PHONY: all venv install run test clean

all: install run 

venv:
	python3 -m venv $(VENV_DIR)

install: venv
	$(PIP) install -r $(REQUIREMENTS_FILE)

add_datas: 
	$(PYTHON) inject_officialsite_datas.py

run: 
	$(PYTHON) app.py