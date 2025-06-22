#!/bin/bash

export LISTEN_ADDRESS=0.0.0.0
export LISTEN_PORT=80
export LEAKY_URL=https://leaky.krondor.org

export DEBUG=False
export PYTHONPATH=/app:$PYTHONPATH

uv run python -m src.__main__

# Exit the script
exit 0
