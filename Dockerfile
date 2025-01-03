# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    virtualenv \
    python3-pip-whl \
    python3-setuptools-whl \
    python3-wheel-whl \
    && rm -rf /var/lib/apt/lists/*

# Copy the bin scripts
COPY bin/ ./bin/

# Make sure the scripts are executable
RUN chmod +x ./bin/*

# Copy the requirements file into the container
COPY requirements.in .

# Install the Python dependencies
RUN /app/bin/install.sh

# Copy the application code
COPY src/ ./src/

# Copy the static assets
COPY static/ ./static/

# Copy the html templates
COPY templates/ ./templates/

# NOTE: you must set the DATABASE_PATH environment variable to the path to the database file
# Create a startup script
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo '/app/bin/run.sh' >> /app/start.sh && \
    chmod +x /app/start.sh

# Expose the port the app runs on
EXPOSE 80

# Set the entrypoint to our startup script
ENTRYPOINT ["/app/start.sh"]
