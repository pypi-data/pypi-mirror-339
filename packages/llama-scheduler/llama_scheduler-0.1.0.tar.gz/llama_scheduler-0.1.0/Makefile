.PHONY: clean clean-test clean-pyc clean-build help install-dev lint test test-all coverage dist
.DEFAULT_GOAL := help

help:
	@echo "Commands:"
	@echo "  clean               remove all build, test, coverage and Python artifacts"
	@echo "  clean-build         remove build artifacts"
	@echo "  clean-pyc           remove Python file artifacts"
	@echo "  clean-test          remove test and coverage artifacts"
	@echo "  install-dev         install the package in development mode"
	@echo "  lint                check style with flake8, black, isort"
	@echo "  test                run tests quickly with the default Python"
	@echo "  test-all            run tests on every Python version with tox"
	@echo "  coverage            check code coverage quickly with the default Python"
	@echo "  docs                generate Sphinx HTML documentation"
	@echo "  dist                builds source and wheel packages"
	@echo "  release             package and upload a release"
	@echo "  example             run an example configuration"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

install-dev:
	pip install -e ".[dev,doc]"

lint:
	ruff check .
	black --check .
	isort --check-only --profile black .

format:
	black .
	isort --profile black .
	ruff check --fix .

test:
	pytest

test-all:
	tox

coverage:
	pytest --cov=llama_scheduler --cov-report=term --cov-report=html

docs:
	rm -f docs/llama_scheduler.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ llama_scheduler
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

dist: clean
	python -m build
	ls -l dist

release: dist
	twine upload dist/*

example:
	# Generate example config if it doesn't exist
	python -m llama_scheduler init example_config.yaml --force
	# Run the scheduler with the example config
	python -m llama_scheduler run example_config.yaml 