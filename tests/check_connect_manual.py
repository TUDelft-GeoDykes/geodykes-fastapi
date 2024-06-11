import os
import pytest
import asyncpg
import asyncio

from dotenv import load_dotenv


# Load the environment variables from .env file
load_dotenv()

async def test_db_connection():
    try:
        # Attempt to connect to the database
        conn = await asyncpg.connect(
            user='postgres',
            password='password',
            database='postgres',
            host=os.getenv("DB_HOST", "db"),
        )
        print("Connected to the database!")
    except Exception as e:
        # Print and assert fail if an exception occurs
        print(f"Failed to connect to database: {e}")
        assert False, f"Database connection failed: {e}"
    else:
        # If successful, close the connection and assert success
        await conn.close()
        assert True

# Run the test
print("Connecting to the database ...")
print("Host: ", os.getenv("DB_HOST", "db"))

asyncio.run(test_db_connection())
