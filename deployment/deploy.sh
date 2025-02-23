#!/bin/bash

set -e

PROJECT_ROOT=$(dirname "$(dirname "$(readlink -f "$0")")")
DEPLOYMENT_FOLDER="$PROJECT_ROOT/deployment"
REQUIREMENTS_FOLDER="$DEPLOYMENT_FOLDER/requirements"
REQUIREMENTS_FILEPATH="$REQUIREMENTS_FOLDER/requirements.txt"

[ ! -d "$REQUIREMENTS_FOLDER" ] && mkdir -p "$REQUIREMENTS_FOLDER"

cd "$DEPLOYMENT_FOLDER"

pip install pip-tools
if ! pip-compile "$PROJECT_ROOT/pyproject.toml" --output-file="$REQUIREMENTS_FILEPATH" --verbose; then
    echo "Failed to compile requirements"
    exit 1
fi

echo "$PROJECT_ROOT" >> "$REQUIREMENTS_FILEPATH"

sam build --debug --template "$PROJECT_ROOT/template.yaml"
sam deploy
