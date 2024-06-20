# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
FLASK = $(VENV_DIR)/bin/flask
TESTS_DIR = tests
REQUIREMENTS_FILE = requirements.txt

# Commandes
.PHONY: all venv install run test clean

# Crée l'environnement virtuel
venv:
	python3 -m venv $(VENV_DIR)

# Install dependency
install: venv
	$(PIP) install -r $(REQUIREMENTS_FILE)

# Launch flask
run: install
	$(PYTHON) app.py