#!/usr/bin/env sh

set -ex

pipenv run flake8 tests transaction_service features *.py
pipenv run python -m pytest
pipenv run behave
