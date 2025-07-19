.PHONY: all format install uninstall

VENV_DIR := .venv

all: format

format:
	ruff check --fix .
	ruff format .

install: venv
	uv pip install -e '.[dev]'

uninstall:
	uv pip uninstall -y tasks-backend
	uv pip freeze | xargs uv pip uninstall -y

venv:
	@if [ ! -f "$(VENV_DIR)/pyvenv.cfg" ]; then \
		echo "Creating new virtual environment..."; \
		uv venv $(VENV_DIR); \
		echo "Virtual environment created in $(VENV_DIR)"; \
	else \
		echo "Virtual environment found in $(VENV_DIR)";\
	fi