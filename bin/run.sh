#!/bin/bash

source venv/bin/activate

export LISTEN_ADDRESS=0.0.0.0
export LISTEN_PORT=80
export LEAKY_URL=https://leaky.krondor.org

export DEBUG=False

python -m src

# Deactivate the virtual environment
deactivate

# Exit the script
exit 0
