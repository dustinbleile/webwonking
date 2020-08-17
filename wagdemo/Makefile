.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


linelength=100
name="webwonking"

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style.  isort and black disagree - so order matters.
	find $(name) -name '*.py' -exec isort --multi-line 3 --trailing-comma -l $(linelength) --atomic {} +
	black --line-length $(linelength) $(name)
	flake8 --max-line-length $(linelength) $(name) tests
	mypy --ignore-missing-imports $(name)

test: ## run tests quickly with the default Python
	python manage.py test
	time pytest --cov tests

coverage: ## check code coverage quickly with the default Python
	coverage run --source wagdemo -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python -m pip install -U setuptools wheel twine
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

pip_install: clean ## pip install
	python -m pip install -U pip setuptools
	python -m pip install -e . --use-feature=2020-resolver

pip_install_dev: clean ## install with dev tools and updates
	python -m pip install -U pip doit setuptools wheel twine
	python -m pip install -e .[dev] -U --use-feature=2020-resolver

