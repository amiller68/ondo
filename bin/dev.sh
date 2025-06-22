#!/bin/bash

# Set environment variables
export HOST_NAME=http://localhost:8001
export LISTEN_ADDRESS=localhost
export LISTEN_PORT=8001
export LEAKY_URL=https://leaky.krondor.org
export DEBUG=True
export DEV_MODE=True
export LOG_PATH=

# Add the project root to PYTHONPATH
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Run the FastAPI server using uv
uv run src/__main__.py

# Exit the script
exit 0
