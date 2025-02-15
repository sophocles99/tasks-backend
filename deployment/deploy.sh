#!/bin/bash

set -e

PROJECT_ROOT=$(dirname "$(dirname "$(realpath "$0")")")
DEPLOYMENT_DIR="$PROJECT_ROOT/deployment"
PROJECT_SRC_DIR="$PROJECT_ROOT/tasks_backend"

cd "$PROJECT_ROOT"

pip install pip-tools
pip-compile ./pyproject.toml --output-file="$DEPLOYMENT_DIR/requirements.txt" --verbose

python -m build
echo "$PROJECT_ROOT/dist/tasks_backend-0.1.0-py3-none-any.whl" >> "$DEPLOYMENT_DIR/requirements.txt"

cd "$DEPLOYMENT_DIR"
sam build --template "$PROJECT_ROOT/template.yaml"
sam deploy
