## Async template on FastAPI and SQLAlchemy 1.4

[![GitHub issues](https://img.shields.io/github/issues/TUDelft-GeoDykes/geodykes-fastapi)](https://github.com/TUDelft-GeoDykes/geodykes-fastapi/issues)
[![GitHub forks](https://img.shields.io/github/forks/TUDelft-GeoDykes/geodykes-fastapi)](https://github.com/TUDelft-GeoDykes/geodykes-fastapi/network)
[![GitHub stars](https://img.shields.io/github/stars/TUDelft-GeoDykes/geodykes-fastapi)](https://github.com/TUDelft-GeoDykes/geodykes-fastapi/stargazers)
[![GitHub license](https://img.shields.io/github/license/TUDelft-GeoDykes/geodykes-fastapi)](https://github.com/TUDelft-GeoDykes/geodykes-fastapi/blob/main/LICENSE)


## Project Description

The **GeoDykes Monitoring System** is a web application designed to monitor the health and behavior of dykes in real-time under varying environmental conditions. The system collects data from a variety of sensors installed on dykes and presents it through an intuitive dashboard. It aims to help researchers and water management authorities make informed decisions for proactive dyke maintenance and disaster prevention.

### Motivation

Dykes play a crucial role in flood protection and water management. Monitoring their behavior in response to changes in weather and environmental conditions is essential for ensuring their long-term stability and safety. This application is a component that helps in the process of tracking, visualizing, and analyzing sensor data, making it easier for stakeholders to maintain dykes proactively.

### Design and Architecture

The **GeoDykes Monitoring System** is architected with modularity and scalability in mind. Key design principles include compliance with the **OpenAPI Specification**, usage of **auto-generated client SDKs**, and a **repository pattern** to decouple the Web API from the underlying database. This ensures flexibility in client development, ease of database substitution, and adherence to industry standards.

**Repository Pattern**: The backend employs a repository pattern that separates the data access logic from the backend logic. The repository pattern abstracts database interactions, making it straightforward to switch to a different database or add support for additional data sources, such as external APIs or file storage.

### Technology Stack Commentary

- **Backend - FastAPI**:  
  The backend is built using FastAPI, a modern and high-performance web framework that supports asynchronous request handling. It provides automatic API documentation and validation based on Python type hints, making it easy to build, test, and maintain RESTful APIs.

- **Database - PostgreSQL**:  
  The data is stored in a PostgreSQL relational database. Due to the backend's decoupled architecture, which utilizes a repository pattern, the database can be easily swapped out or extended to support other databases (e.g., MySQL, MongoDB) or even external data sources like APIs or file storage.

- **Frontend - Dash**:  
  The dashboard is implemented using Dash, a Python framework specifically designed for building data-driven, interactive web applications. The auto-generated client SDK based on the OpenAPI specification ensures seamless communication between the backend and frontend, providing a responsive interface for real-time data visualization and monitoring.

---

## Prerequisites
Make sure to have `poetry`, `docker`, `go-task` and `docker-compose` installed in your system.

### Install python 3.11 or higher
Make sure you have python 3.11 or higher installed in your system. You can check the version of python by running the following command:
```sh
python3 --version
```

## Steps to deploy the app
Check the docker-compose file to see the services that are being deployed, and how they are setup.
1. Make sure to have a `.env-production` file in the root directory with the following variables:
```
# ./.env-production
DB_HOST=db # This is the name of the service in the docker-compose file
DB_USER=postgres
DB_PASS=password
DB_DATABASE=postgres
```
2. Deploy locally with `docker-compose up`
3. To see the webapp docs go to this url: `localhost:8000/docs`


## Local development setup for the backend
After installing everything and all the above works, you can also setup a local setup, to run the application locally and connect to the database container.

### Deploy only database container
```sh
docker-compose up -d db
```


### Activate your environment
```sh
# Activate the environment using poetry
poetry shell
```
## Make sure to load environment variables
```sh
source .env # This will export the environment variables declared in the .env file
echo ${DB_HOST} # should print localhost
```

### Run pytest most tests should pass
```
pytest
```

### Run migrations
In order for the application stack to work, you need to run the migrations. This will create the tables in the database.
```sh
# Run the migrations
alembic upgrade head
```

#### When the model changes during development
When the model changes, you need to create a new migration. This is done by running the following command:
```sh
alembic revision --autogenerate -m "Add a new column"
```

### Run the app
```sh
# Export PYTHONPATH
export PYTHONPATH="$(poetry env info --path)/lib/python3.12/site-packages":$PYTHONPATH

# Export all environment variables with script export-env.sh
source export-env.sh 
poetry run uvicorn app.application:application --reload
```
## Local development setup for the frontend
### Running the Frontend Application in Development Setup

1. **Navigate to the dashboard directory**:
   ```sh
   cd root/dashboard
   ```

2. **Install dependencies and activate the virtual environment**:
   ```sh
   poetry install
   poetry shell
   ```

3. **Run the frontend application**:
   ```sh
   poetry run python geodykes-dash/dash-app.py
   ```

### Access the Dashboard

Open your browser and go to `http://localhost:8050`.
## Licensing and waiver

Licensed under MIT, subject to waiver:

Technische Universiteit Delft hereby disclaims all copyright interest in the program “geodykes-app” (A web application and system to monitor and visualize dykes) written by the Author(s).

Prof.dr.ir. Stefan Aarninkhof, Dean of Civil Engineering and Geosciences

Copyright (c) 2022 Jose Carlos Urra Llanusa, Ching-Yu Chao, Selin Kubilay.



