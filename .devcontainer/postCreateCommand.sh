#!/usr/bin/env sh

set -euxo pipefail

uv sync

git config --unset-all core.hooksPath
uv run pre-commit install --allow-missing-config
