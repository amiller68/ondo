#!/bin/bash

# Install uv if not installed
if ! [ -x "$(command -v uv)" ]; then
	echo 'Error: uv is not installed.' >&2
	echo 'Install uv by running: curl -LsSf https://astral.sh/uv/install.sh | sh' >&2
	exit 1
fi

# Create virtual environment and pin Python version
uv venv
uv python pin 3.12

# Lock and sync dependencies including dev dependencies
uv lock
uv sync --dev

exit 0
