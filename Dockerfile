ARG ENVIRONMENT="prod"
FROM python:3.12-slim

# Install required packages for psycopg2
RUN apt update \
    && apt install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip poetry
RUN useradd --no-create-home --gid root runner

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /code

# Copy dependency files for caching
COPY pyproject.toml .
COPY poetry.lock .

# Install dependencies
RUN if [ "$ENVIRONMENT" = "prod" ]; then \
      poetry install --no-dev; \
    else \
      poetry install; \
    fi

# Copy only the backend-related files
COPY app /code/app
COPY alembic.ini /code/
COPY migrations /code/migrations
COPY tests /code/tests

# Adjust permissions
RUN chown -R runner:root /code && chmod -R g=u /code

# Switch to the runner user
USER runner
