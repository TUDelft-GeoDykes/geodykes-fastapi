## Async template on FastAPI and SQLAlchemy 1.4

[![GitHub issues](https://img.shields.io/github/issues/lesnik512/fast-api-sqlalchemy-template)](https://github.com/lesnik512/fast-api-sqlalchemy-template/issues)
[![GitHub forks](https://img.shields.io/github/forks/lesnik512/fast-api-sqlalchemy-template)](https://github.com/lesnik512/fast-api-sqlalchemy-template/network)
[![GitHub stars](https://img.shields.io/github/stars/lesnik512/fast-api-sqlalchemy-template)](https://github.com/lesnik512/fast-api-sqlalchemy-template/stargazers)
[![GitHub license](https://img.shields.io/github/license/lesnik512/fast-api-sqlalchemy-template)](https://github.com/lesnik512/fast-api-sqlalchemy-template/blob/main/LICENSE)

### Description
Production-ready dockerized async REST API on FastAPI with SQLAlchemy and PostgreSQL

## Prerequisites
Make sure to have `poetry`, `docker`, `go-task` and `docker-compose` installed in your system.

## Key Features
- tests on `pytest` with automatic rollback after each test case
- db session stored in Python's `context variable`
- configs for `mypy`, `pylint`, `isort` and `black`
- `Alembic` for DB migrations
- CI with Github

### After `git clone` run
```bash
task -l  # list of tasks with descriptions
```

### Prepare virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
poetry install
```

# [Poetry](https://python-poetry.org/docs/)

Poetry is python package manager.

Poetry resolve dependencies and conflicts in package and make it fast.

## Basic usage

- `poetry lock` lock dependencies
- `poetry update` lock, update and install dependencies
- `poetry install` for install dependencies from pyproject.toml
- `poetry add <package>` for adding dependency with check on conflicts
- `poetry remove <package>` for remove
- `poetry self update` update poetry

# [Task](https://taskfile.dev/)

Task is a task runner / build tool that aims to be simpler and easier to use than, for example, GNU Make.

## Basic usage

- `task -l` - list of tasks with descriptions
- `task -a` - list of all tasks

## Steps to deploy the app

1. Deploy locally with `docker-compose up`
5. To see the webapp go to this url: `localhost:8000/docs`


## Local development setup
After installing everything and all the above works, you can also setup a local setup, to run the application locally and connect to the database container.

### Activate your environment
```
poetry shell
```
### Run the app script to make sure 
These are things I needed to do in MacOS. You might not to do all these steps in linux.
```bash
source $(poetry env info --path)/bin/activate
python3 app/application.py # Make sure that you can run the app

export PYTHONPATH="$(poetry env info --path)/lib/python3.12/site-packages":$PYTHONPATH
poetry run uvicorn app.application:application --reload

# Make sure to load environment variables
source .env # This will export the environment variables declaed in the .env file
echo ${DB_HOST} # should print localhost
```

