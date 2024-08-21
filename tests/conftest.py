import asyncio
import typing

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.application import application
from app.db.base import engine
from app.db.deps import session_context_var, set_db




@pytest.fixture()
async def db() -> typing.AsyncIterator[AsyncSession]:
    connection = await engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection, expire_on_commit=False, future=True)
    await connection.begin_nested()
    try:
        yield session
    finally:
        if session.in_transaction():
            await transaction.rollback()
        await connection.close()


@pytest.fixture(name="db_context", autouse=True)
def _db_context(db: AsyncSession) -> typing.Iterator[None]:
    token = session_context_var.set(db)
    yield
    session_context_var.reset(token)


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(application) as c:
        yield c
