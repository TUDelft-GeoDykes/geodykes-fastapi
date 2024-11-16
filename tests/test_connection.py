import os

import asyncpg


# @pytest.mark.asyncio
async def test_db_connection() -> None:
    try:
        # Attempt to connect to the database
        conn = await asyncpg.connect(
            user="postgres",
            password="password",
            database="postgres",
            host=os.getenv("DB_HOST", "db"),
        )
    except Exception as e:
        # Print and assert fail if an exception occurs
        msg = f"Database connection failed: {e}"
        raise AssertionError(msg)
    else:
        # If successful, close the connection and assert success
        await conn.close()
        assert True

