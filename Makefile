.PHONY: install test

VENV ?= .venv
PYTHON := $(VENV)/bin/python
PYTEST := $(VENV)/bin/pytest

install:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -r requirements.txt

test:
	PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONNOUSERSITE=1 $(PYTEST) -q
