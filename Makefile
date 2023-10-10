PYTHON = python3

override src = xprun.py

override tests = tests

override venv = .venv

override installed = $(venv)/.installed

.PHONY: setup
setup: $(installed) vscode

.PHONY: format
format: black isort

.PHONY: check
check: lint coverage

.PHONY: lint
lint: black-check isort-check flake8

.PHONY: black
black: $(venv)/bin/black
	$(venv)/bin/black -q $(src) $(tests) setup.py

.PHONY: isort
isort: $(venv)/bin/isort
	$(venv)/bin/isort $(src) $(tests) setup.py

.PHONY: black-check
black-check: $(venv)/bin/black
	$(venv)/bin/black -q --check $(src) $(tests) setup.py

.PHONY: isort-check
isort-check: $(venv)/bin/isort
	$(venv)/bin/isort -c $(src) $(tests) setup.py

.PHONY: flake8
flake8: $(venv)/bin/flake8
	$(venv)/bin/flake8 $(src) $(tests) setup.py

.PHONY: test
test: $(venv)/bin/pytest $(installed)
	$(venv)/bin/pytest

.PHONY: coverage
coverage: $(venv)/bin/pytest $(installed)
	$(venv)/bin/pytest --cov --cov-report=term --cov-report=xml

.PHONY: build
build: $(venv)/bin/pyproject-build
	$(venv)/bin/pyproject-build

.PHONY: vscode
vscode: .vscode/settings.json

# clean tasks -----------------------------------------------------------------
.PHONY: clean
clean: $(shell grep -o '^clean-[^:]*' Makefile)

.PHONY: clean-venv
clean-venv:
	rm -rf $(venv)

.PHONY: clean-pyc
clean-pyc:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -delete

.PHONY: clean-test
clean-test:
	rm -rf .pytest_cache

.PHONY: clean-coverage
clean-coverage: clean-test
	rm -rf .coverage coverage.xml

.PHONY: clean-build
clean-build:
	rm -rf dist src/*.egg-info

.PHONY: clean-vscode
clean-vscode:
	rm -rf .vscode

# venv creation ---------------------------------------------------------------
$(venv)/bin/python:
	$(PYTHON) -m venv $(venv) --clear --without-pip

$(venv)/bin/pip3: $(venv)/bin/python
	$(venv)/bin/python -m ensurepip
	$(venv)/bin/pip3 install -U pip

# project installation --------------------------------------------------------
$(venv)/.installed: $(venv)/bin/pip3
	$(venv)/bin/pip3 install -e . && touch $@

# builder installation --------------------------------------------------------
$(venv)/bin/pyproject-build: $(venv)/bin/pip3
	$(venv)/bin/pip3 install -I build==1.0.3

# checker installation --------------------------------------------------------
$(venv)/bin/black: $(venv)/bin/pip3
	$(venv)/bin/pip3 install -I black==23.9.1

$(venv)/bin/isort: $(venv)/bin/pip3
	$(venv)/bin/pip3 install -I isort==5.12.0

$(venv)/bin/flake8: $(venv)/bin/pip3
	$(venv)/bin/pip3 install -I flake8==6.1.0
	$(venv)/bin/pip3 install -I flake8-black==0.3.6
	$(venv)/bin/pip3 install -I flake8-tidy-imports==4.10.0

$(venv)/bin/pytest: $(venv)/bin/pip3
	$(venv)/bin/pip3 install -I pytest==7.4.2
	$(venv)/bin/pip3 install -I pytest-cov==4.1.0

# editor setting generation ---------------------------------------------------
.vscode/settings.json:
	mkdir -p .vscode
	echo '{'                                                         > .vscode/settings.json
	echo '  "coverage-gutters.showLineCoverage": true,'             >> .vscode/settings.json
	echo '  "python.testing.pytestEnabled": true,'                  >> .vscode/settings.json
	echo '  "python.defaultInterpreterPath": "$(venv)/bin/python",' >> .vscode/settings.json
	echo '}'                                                        >> .vscode/settings.json
