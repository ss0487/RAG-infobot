# Build from /data/rag-app/streamlit_server
# Sticking to a single-stage build as there isn't any extra benefit with multiple stages for this application

# Use the Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /streamlit_server

# Copy all the app files, which includes requirements.txt
COPY . .

# Copy nginx proxy configuration for streamlit_server
COPY ./streamlit.nginx.conf /etc/nginx/conf.d/default.conf

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    nginx \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r ./requirements.txt

# Run the Streamlit app
ENTRYPOINT ["sh", "./entrypoint.sh"]