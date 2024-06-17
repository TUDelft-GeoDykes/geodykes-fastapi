# conftest.py
import pytest
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import reflection
from sqlalchemy.orm import sessionmaker
from app.db.base import Base


@pytest.fixture(scope="session")
def engine():
    # Setup an engine connected to the in-memory or test database
    return create_engine('sqlite:///:memory:', echo=True)

@pytest.fixture(scope="session")
def tables(engine):
    # Create all tables in the database
    Base.metadata.create_all(engine) # This creates all tables in the database
    return engine

@pytest.fixture(scope="session")
def inspector(engine):
    return reflection.Inspector.from_engine(engine) # This we need to check that all tables are in the database

@pytest.fixture(scope="function")
def session(tables):
    # Create a new session for each test
    connection = tables.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
