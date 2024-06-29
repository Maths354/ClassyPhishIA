VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
GUNICORN = $(VENV_DIR)/bin/gunicorn
TESTS_DIR = tests
REQUIREMENTS_FILE = requirements.txt

.PHONY: all venv install run test clean

all: install run 

venv:
	python3 -m venv $(VENV_DIR)

install: venv
	$(PIP) install -r $(REQUIREMENTS_FILE)

add_datas: 
	$(PYTHON) inject_db/inject_officialsite_datas.py

run: 
	$(GUNICORN) -w 4 -b 0.0.0.0:8000 wsgi:app

dev: 
	$(PYTHON) wsgi.py