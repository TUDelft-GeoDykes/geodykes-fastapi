# How to run the app direcctly without having to build it in a container
Given the structure of your `Settings` class in the FastAPI project, it's clear that your application uses `pydantic_settings.BaseSettings` for configuration, which is a good practice for managing settings via environment variables and other sources. Your database connection settings are dynamically assembled into a SQLAlchemy Database URL (`db_dsn`), which is ideal for connecting to your database, whether it's running in a Docker container or natively on your host machine.

To connect your FastAPI application running directly on your local machine to a PostgreSQL database running in a Docker container (as set up in your `docker-compose.yml`), you need to adjust the `db_host` to point to `localhost` (or the appropriate host address where your Docker is running if you're using Docker Toolbox or a similar setup on Windows). However, since your application might be configured to read these settings from environment variables automatically, you can override them without modifying the code.

### Running FastAPI with Local Database Connection

1. **Override Database Host for Local Development**: 
    - When running your FastAPI app locally, you can override the `db_host` to `localhost` using an environment variable. Pydantic's `BaseSettings` class automatically loads environment variables that match the field names in your settings class.
    - Set the environment variable `DB_HOST=localhost` before running your application. How you set this variable depends on your operating system:
      - On Linux or macOS:
        ```sh
        export DB_HOST=localhost
        ```
      - On Windows Command Prompt:
        ```cmd
        set DB_HOST=localhost
        ```
      - On Windows PowerShell:
        ```powershell
        $env:DB_HOST="localhost"
        ```

2. **Ensure the Database Container is Running**:
    - Make sure the PostgreSQL container is running as configured in your `docker-compose.yml`. You can start it with:
      ```sh
      docker-compose up -d db
      ```

3. **Run Your FastAPI Application**:
    - Start your FastAPI app with the overridden environment variable in place. If you're using a virtual environment, ensure it's activated. Then start your application (assuming Uvicorn as the ASGI server):
      ```sh
      uvicorn app.main:app --reload
      ```
    - This command assumes your FastAPI app is defined in a module called `main` within an `app` package and that you're using the `--reload` option for live reloading during development.

### Additional Considerations

- **Environment Variables for Other Settings**: Similar to `db_host`, you can override other settings like `db_user`, `db_password`, `db_port`, and `db_database` using environment variables (`DB_USER`, `DB_PASSWORD`, `DB_PORT`, `DB_DATABASE`) if your local setup differs from your containerized setup.
- **Persistence**: Your database data will persist across container restarts due to the volume configuration in your `docker-compose.yml`. This is crucial for maintaining state during development.
- **Security**: Be mindful of security implications when connecting to your database and ensure that your database credentials are securely managed, especially in production environments.

This setup provides a flexible development environment, allowing you to leverage the benefits of containerization for your database while running your application directly on your host machine for easier debugging and development.




Running your FastAPI app directly in the terminal for local development while connecting to a database running in a Docker container can streamline your development process, providing more immediate feedback and simplifying debugging. Here's how you can set up this development environment:

### 1. **Set Up Your Database Container**

First, ensure you have Docker installed and running on your machine. Then, set up your database container. Here's an example using PostgreSQL, but the approach is similar for other databases:

1. Pull the PostgreSQL Docker image:
   ```sh
   docker pull postgres
   ```

2. Run a PostgreSQL container. Replace `your_password` with a secure password:
   ```sh
   docker run --name some-postgres -e POSTGRES_PASSWORD=your_password -d -p 5432:5432 postgres
   ```
   
   This command starts a PostgreSQL container named `some-postgres`, sets the default password, and maps port `5432` on the container to port `5432` on your host, making the database accessible to applications running on your host machine.

### 2. **Configure FastAPI to Connect to the Database Container**

In your FastAPI application, configure the database connection to point to the localhost's port `5432` where the PostgreSQL container is mapped. 

- For a SQLAlchemy database URL in your FastAPI app settings, it would look something like this:
  ```python
  SQLALCHEMY_DATABASE_URL = "postgresql://postgres:your_password@localhost/postgres"
  ```
  This assumes you're connecting with the default `postgres` user to the default `postgres` database. Adjust the connection string according to your setup.

### 3. **Run Your FastAPI App Locally**

With your database running in a Docker container and your FastAPI app configured to connect to it, you can now run your FastAPI app directly on your host machine (outside Docker).

1. If you haven’t already, ensure you have FastAPI and Uvicorn (an ASGI server for running FastAPI) installed in your development environment. It's often recommended to use a virtual environment (`venv`) for Python projects:
   ```sh
   pip install fastapi uvicorn
   ```

2. Start your FastAPI application using Uvicorn. Navigate to your project directory in the terminal and run:
   ```sh
   uvicorn app.main:app --reload
   ```
   Replace `app.main:app` with the correct path to your FastAPI app instance. The `--reload` flag enables auto-reload on code changes, which is useful during development.

### 4. **Development Workflow**

- **Code Changes**: Make changes to your FastAPI application code. Uvicorn with `--reload` will automatically restart the server on code changes, allowing you to immediately see the effects.
  
- **Database Interactions**: Perform database operations from your FastAPI app. The app will communicate with the PostgreSQL server running in the Docker container.

- **Testing**: You can test your API endpoints using tools like Swagger UI (automatically available at `http://localhost:8000/docs` with FastAPI), Postman, or directly from your frontend application.

### 5. **Additional Tips**

- **Network Issues**: If you encounter issues connecting to the database from your host machine, ensure the Docker container is running and the port mapping is correctly configured. Use `docker ps` to verify the container's status and port mappings.
  
- **Environment Variables**: Consider using environment variables for database URLs and other sensitive/configurable data, making your application more flexible and secure.

- **Database GUI Tools**: You might find it helpful to use a database GUI tool (e.g., pgAdmin for PostgreSQL) to connect to your database container for direct database management, query execution, and debugging during development.

This setup provides the flexibility and speed of local development for your FastAPI app while still leveraging Docker for database services, combining the best of both worlds for a productive development workflow.

## Troubleshooting setup
To check if the database in Docker is accessible (Point 1) and to ensure that environment variables are set correctly (Point 2), follow these detailed steps:

### 1. Checking Database Accessibility

**Step A: Ensure the Docker Container is Running**

First, make sure your PostgreSQL container is running. Use this command to list running containers:

```bash
docker ps
```

Look for your PostgreSQL container in the list. If it's not running, start it using:

```bash
docker-compose up db
```

**Step B: Try Connecting to the Database**

Use a database client tool like `psql` to test connecting to your PostgreSQL instance. Here’s how you can do it from the command line:

```bash
psql -h localhost -U postgres -d postgres -p 5432
```

You'll be prompted for a password, which, according to your Docker Compose file, should be "password".

**Troubleshooting Connection Issues**:

- **Port Not Exposed**: Ensure that port 5432 is listed under `ports` in your `db` service in the Docker Compose file. It should look like `5432:5432`.
- **Firewall or Network Restrictions**: Sometimes, local firewalls or network settings can block ports. Make sure port 5432 is open on your local machine.
- **Incorrect Credentials**: Verify that the username and password are set as expected in both your Docker Compose and the command you use to connect.

### 2. Ensuring Environment Variables Are Set Correctly

**Step A: Setting Environment Variables**

To dynamically set the database host through an environment variable (`DB_HOST`), you can add this line to your terminal session, to a script that starts your application, or to an `.env` file in your project directory:

```bash
export DB_HOST=localhost
```

**Step B: Verifying the Environment Variable**

You can verify that an environment variable is set by echoing it in the terminal:

```bash
echo $DB_HOST
```

The output should be `localhost` if set correctly.

**Using `.env` Files**:

If your project uses a `.env` file and libraries like `python-dotenv` to load these settings:

1. Add the variable to the `.env` file:

   ```
   DB_HOST=localhost
   ```

2. Ensure your application loads this file. If using FastAPI with Pydantic, as your settings setup suggests, `python-dotenv` or similar should be configured to load these values when your application starts.

**Verifying in Application**:

Add a debug print in your application to print out the database host when it initializes:

```python
print("Database Host:", settings.db_host)
```

This will confirm that the application is using the correct environment variable at runtime.

### Running and Testing

After confirming the database connectivity and ensuring the environment variables are set and correctly loaded by your application, run your application as usual. Check the debug output to ensure that the `DB_HOST` is correctly being used to form your database connection strings and that there are no errors connecting to the database.

These checks will help ensure your local development setup using Docker for the database and local execution for the application works smoothly.

## Troubleshooting notes
- It might be that fastapi appears as a dependency but then when running the application it cannot find it. I solved it by uninstalling with poetry and adding it back.