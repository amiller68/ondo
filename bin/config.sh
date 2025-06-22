#!/bin/bash

# Configuration settings for bin scripts

# Development server port
export DEV_SERVER_PORT=${DEV_SERVER_PORT:-8000}

# Python virtual environment
export VENV_PATH="venv"

# Project name
export PROJECT_NAME="ondo"

# Docker settings
export DOCKER_IMAGE_NAME="${PROJECT_NAME}-app"
export DOCKER_TAG="latest"