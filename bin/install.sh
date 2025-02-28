#!/bin/bash

# Install virtualenv if not installed
if ! [ -x "$(command -v virtualenv)" ]; then
	echo 'Error: virtualenv is not installed.' >&2
	exit 1
fi

virtualenv venv --python=python3.12

source venv/bin/activate
pip install pip-tools
pip-compile requirements.in -o requirements.txt
pip install -r requirements.txt

deactivate

exit 0
