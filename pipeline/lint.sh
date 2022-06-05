#!/bin/bash

set -eo pipefail

# Allow usage from multiple directories (TODO)
CURRENT_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

poetry run pylint -j 0 $CURRENT_DIRECTORY/../correpy
poetry run mypy --show-error-codes  $CURRENT_DIRECTORY/../correpy
poetry run isort --profile black --line-length=120 --check-only $CURRENT_DIRECTORY/../correpy
poetry run black --check --line-length 120 $CURRENT_DIRECTORY/../correpy
