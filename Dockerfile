# Use the official uv Python runtime as the base image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the bin scripts
COPY bin/ ./bin/

# Make sure the scripts are executable
RUN chmod +x ./bin/*

# Copy the dependency files into the container
COPY pyproject.toml .

# Install the Python dependencies
RUN /app/bin/install.sh

# Copy the application code
COPY src/ ./src/

# Copy the static assets
COPY static/ ./static/

# Copy the styles (for potential Tailwind compilation)
COPY styles/ ./styles/

# Copy the Tailwind config
COPY tailwind.config.js .

# Copy the html templates
COPY templates/ ./templates/

# Create a startup script
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo '/app/bin/run.sh' >> /app/start.sh && \
    chmod +x /app/start.sh

# Expose the port the app runs on
EXPOSE 80

# Set the entrypoint to our startup script
ENTRYPOINT ["/app/start.sh"]