PWD = $(shell pwd)
VENV = $(PWD)/.venv
BIN_FLAKE8 = $(VENV)/bin/flake8
BIN_ISORT = $(VENV)/bin/isort

.PHONY: clean virtualenv test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete
	rm -rf $(VENV)

flake8:
	$(BIN_FLAKE8)

isort:
	$(BIN_ISORT) **/*.py --filter-files --interactive

isort_check:
	$(BIN_ISORT) **/*.py --filter-files --check-only

virtualenv:
	virtualenv --prompt '|> figfind <| ' env
	env/bin/pip install -r requirements-dev.txt
	env/bin/python setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

test:
	python -m pytest \
		-v \
		--cov=figfind \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t figfind:latest .

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*
