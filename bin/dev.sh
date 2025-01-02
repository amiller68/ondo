#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export HOST_NAME=http://localhost:8000
export LISTEN_ADDRESS=localhost
export LISTEN_PORT=8000
export LEAKY_URL=https://leaky.krondor.org
export DEBUG=True
export DEV_MODE=True
export LOG_PATH=

# Add the project root to PYTHONPATH
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Run the FastAPI server in the background
python -m src

# Deactivate virtual environment
deactivate

# Exit the script
exit 0
