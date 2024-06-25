import pytest
# Assume this is in models.py or a similar module
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base


@pytest.fixture(scope="session")
def dummy_engine():
    # New declarative base
    NewBase = declarative_base()

    class Dummy(NewBase):
        __tablename__ = 'dummy'
        id = Column(Integer, primary_key=True)
        name = Column(String)

    # Ensure a single instance of the engine is used across all tests
    engine = create_engine('sqlite:///:memory:', echo=True)
    NewBase.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session")
def inspector_dummy(dummy_engine):
    from sqlalchemy import inspect
    return inspect(dummy_engine)

# test_database.py
def test_dummy_table_exist(inspector_dummy):
    # List of expected tables
    expected_tables = {'dummy'}

    # Get the set of actual tables from the database
    actual_tables = set(inspector_dummy.get_table_names())

    # Assert that every expected table is in the set of actual tables
    assert expected_tables.issubset(actual_tables), f"Missing tables: {expected_tables - actual_tables}"

@pytest.fixture(scope="session")
def inspector(tables):
    from sqlalchemy import inspect
    return inspect(tables)

# test_database.py
def test_tables_exist(inspector):
    # List of expected tables
    expected_tables = {'dyke', 'crossection', 'topology'}

    # Get the set of actual tables from the database
    actual_tables = set(inspector.get_table_names())

    # Assert that every expected table is in the set of actual tables
    assert expected_tables.issubset(actual_tables), f"Missing tables: {expected_tables - actual_tables}"
