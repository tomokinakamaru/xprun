PYTHON := python3

override src = xptools

override test_deps =

override venv = venv

override bin = $(venv)/bin

override pip = $(bin)/pip

override python = $(bin)/python

# -----------------------------------------------------------------------------
.PHONY: setup
setup: install

.PHONY: setup-dev
setup-dev: setup $(bin)/flake8 $(bin)/mypy vscode

.PHONY: check
check: flake8 mypy

.PHONY: clean
clean: $(shell grep -o '^clean-[^:]*' Makefile)
	rm -rf $(venv)

.PHONY: clean-pyc
clean-pyc:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -delete

# install ---------------------------------------------------------------------
.PHONY: install
install: $(venv)/.installed

.PHONY: clean-install
clean-install:
	rm -rf $(venv)/.installed build *.egg-info

$(venv)/.installed: $(pip)
	$< install -e . && touch $@

$(pip): $(python)
	curl -sfS https://bootstrap.pypa.io/get-pip.py | $<

$(python):
	$(PYTHON) -m venv $(venv) --without-pip

# flake8 ----------------------------------------------------------------------
.PHONY: flake8
flake8: $(bin)/flake8
	$< setup.py $(src)

$(bin)/flake8: $(pip)
	$< install flake8

# mypy ------------------------------------------------------------------------
.PHONY: mypy
mypy: $(bin)/mypy
	$< setup.py $(src)

.PHONY: clean-mypy
clean-mypy:
	rm -rf .mypy_cache

$(bin)/mypy: $(pip)
	$< install mypy

# vscode ----------------------------------------------------------------------
.PHONY: vscode
vscode: .vscode/.gitignore .vscode/settings.json

.PHONY: clean-vscode
clean-vscode:
	rm -rf .vscode

.vscode:
	mkdir -p $@

.vscode/.gitignore: | .vscode
	echo '*' > $@

.vscode/settings.json: | .vscode
	echo '{' > $@
	echo '  "python.linting.flake8Enabled": true,' >> $@
	echo '  "python.linting.mypyEnabled": true,' >> $@
	echo '  "python.defaultInterpreterPath": "$(python)"' >> $@
	echo '}' >> $@
