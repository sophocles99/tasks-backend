.PHONY: format install uninstall

all: format

format:
	ruff check --fix .
	ruff format .

install:
	pip install -e '.[dev]'

uninstall:
	pip uninstall -y tasks-backend
