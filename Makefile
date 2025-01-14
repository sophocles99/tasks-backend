.PHONY: all format install uninstall

all: format

format:
	ruff check --fix .
	ruff format .

install:
	python -m pip install --upgrade pip
	pip install -e '.[dev]'

uninstall:
	pip uninstall -y tasks-backend
	pip freeze | xargs pip uninstall -y
