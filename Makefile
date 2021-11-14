PWD = $(shell pwd)
VENV = $(PWD)/.venv
BIN_FLAKE8 = $(VENV)/bin/flake8
BIN_ISORT = $(VENV)/bin/isort

.PHONY: clean flake8 isort isort_check test

clean:
	find . -name '*.py[co]' -delete
	rm -rf $(VENV)

flake8:
	$(BIN_FLAKE8)

isort:
	$(BIN_ISORT) **/*.py --filter-files --interactive

isort_check:
	$(BIN_ISORT) **/*.py --filter-files --check-only

test:
	python -m pytest \
		-v \
		--cov=figfind \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/
