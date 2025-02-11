# Build from /data/rag-app/flask_api
# Inside the Docker, app has to run one folder above the folder containing the app factory
# The required files are mounted in /flask_api/generate,
#   so the gunicorn command will run in /flask_api.

# Use the Python base image
FROM scratch AS builder-dev

# Set the working directory
WORKDIR /flask_api

# Copy requirements file
COPY requirements.txt requirements.txt

# Copy entrypoint shell script file
COPY entrypoint.sh entrypoint.sh

# Copy the rest of the application code
COPY . ./generate

# Multi-stage build: Stage 2 (final)
FROM python:3.10-slim AS dev

# Copy the application files from the previous stage
COPY --from=builder-dev /flask_api /flask_api

# Install apt dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    nginx \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /flask_api/requirements.txt \
    && rm /etc/nginx/sites-enabled/default

# Copy the nginx config files
COPY --from=builder-dev /flask_api/generate/nginx-configs /etc/nginx/conf.d

# Run the Flask app
ENTRYPOINT ["sh", "/flask_api/generate/entrypoint.sh"]