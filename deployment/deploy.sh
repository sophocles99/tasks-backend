#!/bin/bash

set -e

PROJECT_ROOT=$(dirname "$(dirname "$(readlink -f "$0")")")
REQUIREMENTS_FILEPATH="lambda-requirements/requirements.txt"

cd "$PROJECT_ROOT/deployment"

pip install pip-tools
pip-compile ../pyproject.toml --output-file="$REQUIREMENTS_FILEPATH" --verbose
echo "$PROJECT_ROOT" >> "$REQUIREMENTS_FILEPATH"

sam build --debug --template ../template.yaml
sam deploy
