# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Install required packages for dependencies (e.g., psycopg2)
RUN apt update \
    && apt install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Poetry
RUN pip install --no-cache-dir --upgrade pip poetry

# Disable Poetry's virtual environments
ENV POETRY_VIRTUALENVS_CREATE=false

# Set the working directory
WORKDIR /app/dashboard

# Copy dependency files for Poetry
COPY ./dashboard/pyproject.toml ./pyproject.toml
COPY ./dashboard/poetry.lock ./poetry.lock

# Copy the dashboard and sdk directories explicitly
COPY ./dashboard /app/dashboard
COPY ./sdk /app/sdk

# Debug file placement
RUN echo "Contents of /app/dashboard:" && ls -la /app/dashboard

# Install dependencies
RUN poetry install

# Adjust permissions
RUN chown -R root:root /app && chmod -R 755 /app

# Create a user for running the app
RUN useradd --no-create-home --gid root runner

# Switch to the runner user
USER runner

# Command will be defined in docker-compose.yml
