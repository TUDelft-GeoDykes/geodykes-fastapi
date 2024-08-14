"""
This conftest.py file is a central configuration file for pytest, containing
fixtures that are shared across multiple test modules. Fixtures are a powerful 
feature of pytest that allow developers to create reusable test setups, manage 
test data, and handle complex dependencies in a clean and modular way.

## Why Use Fixtures?

Fixtures in pytest provide a way to set up a known state before tests run and 
to clean up afterward. They help to:

1. **Avoid Repetition:** Common setup code is written once and reused across multiple tests.
2. **Improve Readability:** Test code becomes cleaner, focusing only on the actual testing logic.
3. **Ensure Isolation:** Fixtures help in maintaining test isolation by providing a fresh environment for each test, ensuring that tests do not interfere with each other.
4. **Manage Complexity:** When tests require complex setups, fixtures can simplify the process by abstracting away the setup details.

In this file, we define various fixtures related to database setup, such as creating 
SQLAlchemy sessions, setting up in-memory SQLite databases, and creating specific 
data models like Dykes, Topologies, and Crossections.

Each fixture is defined with a specific scope (`session`, `function`, etc.), indicating 
how often the fixture setup should be executed. For example, session-scoped fixtures 
are executed once per test session, while function-scoped fixtures are executed for 
each test function.

The fixtures provided here are fundamental to the test suite, ensuring that each test 
runs in a consistent, isolated environment, with necessary dependencies and data set up 
in advance.

## Fixtures Defined:

- **engine**: Sets up a connection to an in-memory SQLite database.
- **tables**: Creates all tables in the database schema.
- **inspector**: Provides a database inspector for schema introspection.
- **session**: Manages SQLAlchemy sessions, providing transaction management for each test.
- **topology**: Creates and returns a simple Topology object.
- **topologies**: Dynamically creates multiple Topology objects based on test parameters.
- **dyke**: Creates and returns a Dyke object.
- **crossection_no_layers**: Creates and returns a Crossection object with no layers.
- **crossection**: Creates and returns a Crossection object with multiple layers.
- **timestamp**: Provides a fixed timestamp for testing purposes.
- **unit_of_measure**: Creates and returns a UnitOfMeasure object.
- **reading**: Creates and returns a Reading object associated with a Crossection.
- **sensor_type**: Creates and returns a SensorType object.
- **location_in_topology**: Creates and returns a LocationInTopology object.
- **sensor**: Creates and returns a Sensor object.
"""

import datetime
import json

import pytest
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.orm import sessionmaker

from app.apps.dykes.models import Topology
from app.db.base import Base


@pytest.fixture(scope="session")
def engine():
    """
    Pytest fixture to create a SQLAlchemy engine connected to an in-memory SQLite database.

    This fixture is executed once per test session. It sets up a connection to a
    SQLite in-memory database which is perfect for testing because it provides a
    clean database for each test run.

    Returns:
        Engine: A SQLAlchemy engine instance connected to the in-memory database.
    """
    return create_engine("sqlite:///:memory:", echo=False)


@pytest.fixture(scope="session")
def tables(engine):
    """
    Pytest fixture to create all database tables.

    This fixture runs once per test session and uses the provided SQLAlchemy engine
    to create all tables defined in the `Base` metadata. This ensures that the database
    schema is set up before any tests are executed.

    Args:
        engine: The SQLAlchemy engine instance provided by the `engine` fixture.

    Returns:
        Engine: The same SQLAlchemy engine instance, now with all tables created.
    """
    Base.metadata.create_all(engine)  # This creates all tables in the database
    return engine


@pytest.fixture(scope="session")
def inspector(engine):
    """
    Pytest fixture to create a SQLAlchemy inspector for database introspection.

    This fixture provides an inspector instance that can be used to introspect the
    database schema, such as checking for the existence of tables or columns.

    Args:
        engine: The SQLAlchemy engine instance provided by the `engine` fixture.

    Returns:
        Inspector: A SQLAlchemy Inspector instance for the provided engine.
    """
    return reflection.Inspector.from_engine(engine)


@pytest.fixture(scope="function")
def session(tables):
    """
    Pytest fixture to manage a SQLAlchemy session for each test function.

    This fixture creates a new SQLAlchemy session for every test function,
    ensuring that each test is isolated in its own transaction context.

    The fixture operates as follows:
    1. Establishes a connection to the database using the `tables` object, which
       is typically an instance of `sqlalchemy.Engine` or `sqlalchemy.MetaData`.
    2. Begins a new transaction on the connection, ensuring that all database
       operations within the test are executed within this transaction.
    3. Creates a new SQLAlchemy session bound to the current connection, allowing
       ORM operations to be performed within the test.
    4. Yields the session to the test function, allowing it to interact with the
       database.

    After the test function completes:
    - The session is closed, releasing any resources held by it.
    - If the transaction is still active, it is rolled back to undo any changes made
      during the test. This ensures that the database state is reset, maintaining test
      isolation and repeatability.
    - The database connection is then closed.

    This setup helps prevent database side effects between tests, ensuring that each
    test starts with a clean state.

    Args:
        tables: A SQLAlchemy `Engine` or `MetaData` object used to connect to the
                database and manage the session.

    Yields:
        session: A SQLAlchemy session instance for use in the test function.
    """
    connection = tables.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    try:
        yield session
    finally:
        session.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()


# TOPOLOGY FIXTURES
TOPOLOGY_BASE_POINTS = [
        {"x": 1, "y": 100},
        {"x": 2, "y": 200},
        {"x": 3, "y": 300},
        {"x": 4, "y": 400},
        {"x": 5, "y": 500},
        {"x": 6, "y": 600},
    ]

# One simple topology
@pytest.fixture(scope="function")
def topology(session):
    """
    Pytest fixture to create and commit a simple Topology object.

    This fixture creates a Topology object with predefined coordinates,
    adds it to the session, and commits it to the database. It then retrieves
    the object to ensure it was correctly saved and returns it for use in tests.

    Args:
        session: The SQLAlchemy session provided by the `session` fixture.

    Returns:
        Topology: The created and committed Topology object.
    """
    topo = Topology(coordinates=TOPOLOGY_BASE_POINTS)
    session.add(topo)
    session.commit()

    retrieved = session.query(Topology).filter_by(id=topo.id).first()
    assert retrieved.coordinates == TOPOLOGY_BASE_POINTS
    return retrieved


# Helper function to generate topologies
def generate_topologies(num_topologies, y_distance) -> list:
    """
    Helper function to generate a list of topologies with adjusted y-coordinates.

    This function generates a specified number of topologies by adjusting the
    y-values of a base set of points. Each topology's y-values are shifted by
    a specified distance to simulate different layers or positions.

    Args:
        num_topologies (int): The number of topologies to generate.
        y_distance (int): The distance to shift the y-values for each subsequent topology.

    Returns:
        list: A list of topologies, where each topology is a list of coordinate dictionaries.
    """
    topologies = []

    # Define the initial set of points for the first topology (surface of the earth)
    base_points = TOPOLOGY_BASE_POINTS

    for i in range(num_topologies):
        # Adjust the y-values for each subsequent topology
        points = [
            {"x": point["x"], "y": point["y"] - i * y_distance} for point in base_points
        ]
        topologies.append(points)

    return topologies


# Fixture to instantiate Topology objects dynamically
@pytest.fixture(scope="function")
def topologies(request, session):
    """
    Pytest fixture to create multiple Topology objects based on test parameters.

    This fixture dynamically generates and creates a specified number of Topology
    objects with adjusted y-coordinates. It then commits these objects to the database
    and returns them for use in tests.

    Args:
        request: The pytest request object that contains parameters for this fixture.
        session: The SQLAlchemy session provided by the `session` fixture.

    Returns:
        list: A list of created and committed Topology objects.
    """
    num_topologies, y_distance = request.param
    topology_gen = generate_topologies(num_topologies, y_distance)

    serialized = json.dumps(topology_gen)
    deserialized = json.loads(serialized)
    assert topology_gen == deserialized

    topo_objects = []
    for topology in topology_gen:
        topo = Topology(coordinates=topology)
        session.add(topo)
        session.commit()
        retrieved = session.query(Topology).filter_by(id=topo.id).first()
        assert retrieved.coordinates == topology
        topo_objects.append(retrieved)

    return topo_objects


# DYKE FIXTURES


# Create a dyke fixture
@pytest.fixture(scope="function")
def dyke(session):
    """
    Pytest fixture to create and commit a Dyke object.

    This fixture creates a Dyke object with a predefined name and description,
    adds it to the session, and commits it to the database. It then retrieves
    the object to ensure it was correctly saved and returns it for use in tests.

    Args:
        session: The SQLAlchemy session provided by the `session` fixture.

    Returns:
        Dyke: The created and committed Dyke object.
    """
    from app.apps.dykes.models import Dyke

    dyk = Dyke(name="test dyke", description="This is our testing dyke")

    session.add(dyk)
    session.commit()

    retrieved = session.query(Dyke).filter_by(id=dyk.id).first()
    assert retrieved == dyk

    return retrieved


# A simple crossection that with no layers
@pytest.fixture(scope="function")
def crossection_no_layers(session, dyke, topology):
    """
    Pytest fixture to create and commit a simple Crossection object with no layers.

    This fixture creates a Crossection object associated with a Dyke and a Topology,
    adds it to the session, and commits it to the database. It then retrieves the object
    to ensure it was correctly saved and returns it for use in tests.

    Args:
        session: The SQLAlchemy session provided by the `session` fixture.
        dyke: The Dyke object provided by the `dyke` fixture.
        topology: The Topology object provided by the `topology` fixture.

    Returns:
        Crossection: The created and committed Crossection object.
    """
    from app.apps.dykes.models import Crossection

    cross = Crossection(
        dyke_id=dyke.id,
        name="test crossection",
        description="empty description",
        topology=topology.id,
    )

    session.add(cross)
    session.commit()

    retrieved = session.query(Crossection).filter_by(id=cross.id).first()
    assert retrieved == cross
    return retrieved


@pytest.fixture(scope="function")
def crossection(session, dyke, topologies):
    """
    Pytest fixture to create and commit a Crossection object with multiple layers.

    This fixture creates a Crossection object associated with a Dyke and the first
    Topology in a list of Topologies, adds it to the session, and commits it to the
    database. It then retrieves the object to ensure it was correctly saved and
    returns it for use in tests.

    Args:
        session: The SQLAlchemy session provided by the `session` fixture.
        dyke: The Dyke object provided by the `dyke` fixture.
        topologies: A list of Topology objects provided by the `topologies` fixture.

    Returns:
        Crossection: The created and committed Crossection object.
    """
    from app.apps.dykes.models import Crossection

    topology = topologies[0]
    cross = Crossection(dyke_id=dyke.id, name="test crossection", topology=topology.id)

    session.add(cross)
    session.commit()

    retrieved = session.query(Crossection).filter_by(id=cross.id).first()
    assert retrieved == cross
    return retrieved


# READING FIXTURES
@pytest.fixture(scope="session")
def timestamp():
    """
    Pytest fixture to provide a fixed timestamp for testing.

    This fixture returns a fixed datetime object, useful for testing scenarios
    where a consistent timestamp is required.

    Returns:
        datetime: A fixed datetime object representing '26 Sep 2022'.
    """
    return datetime.datetime.strptime("26 Sep 2022", "%d %b %Y")


@pytest.fixture(scope="function")
def unit_of_measure(session):
    """
    Pytest fixture to create and commit a UnitOfMeasure object.

    This fixture creates a UnitOfMeasure object with predefined attributes,
    adds it to the session, and commits it to the database. It then retrieves
    the object to ensure it was correctly saved and returns it for use in tests.

    Args:
        session: The SQLAlchemy session provided by the `session` fixture.

    Returns:
        UnitOfMeasure: The created and committed UnitOfMeasure object.
    """
    from app.apps.dykes.models import UnitOfMeasure

    unit = UnitOfMeasure(unit="mm", description="Description of this unit of measure")

    session.add(unit)
    session.commit()

    retrieved = session.query(UnitOfMeasure).filter_by(id=unit.id).first()
    assert retrieved == unit
    return retrieved


@pytest.fixture(scope="function")
def reading(
    session, crossection_no_layers, timestamp, unit_of_measure, location_in_topology
):
    """
    Pytest fixture to create and commit a Reading object.

    This fixture creates a Reading object associated with a Crossection,
    a UnitOfMeasure, and a specific location within the Topology. The Reading is
    timestamped with a fixed datetime and saved to the database. The object is
    then retrieved to ensure it was correctly saved and returned for use in tests.

    Args:
        session: The SQLAlchemy session provided by the `session` fixture.
        crossection_no_layers: The Crossection object provided by the `crossection_no_layers` fixture.
        timestamp: The fixed timestamp provided by the `timestamp` fixture.
        unit_of_measure: The UnitOfMeasure object provided by the `unit_of_measure` fixture.
        location_in_topology: The LocationInTopology object provided by the `location_in_topology` fixture.

    Returns:
        Reading: The created and committed Reading object.
    """
    from app.apps.dykes.models import Reading

    read = Reading(
        crossection_id=crossection_no_layers.id,
        location_in_topology_id=location_in_topology.id,
        unit=unit_of_measure,
        value=10,
        time=timestamp,
    )

    session.add(read)
    session.commit()

    retrieved = session.query(Reading).filter_by(id=read.id).first()
    assert retrieved == read
    return retrieved


@pytest.fixture(scope="function")
def sensor_type(session):
    """
    Pytest fixture to create and commit a SensorType object.

    This fixture creates a SensorType object with predefined attributes,
    adds it to the session, and commits it to the database. It then retrieves
    the object to ensure it was correctly saved and returns it for use in tests.

    Args:
        session: The SQLAlchemy session provided by the `session` fixture.

    Returns:
        SensorType: The created and committed SensorType object.
    """
    from app.apps.dykes.models import SensorType

    sensor = SensorType(name="TempSensor", details="measures temperature")
    session.add(sensor)
    session.commit()

    retrieved = session.query(SensorType).filter_by(id=sensor.id).first()
    assert retrieved == sensor
    return retrieved


@pytest.fixture(scope="function")
def location_in_topology(session, crossection_no_layers):
    """
    Pytest fixture to create and commit a LocationInTopology object.

    This fixture creates a LocationInTopology object with a predefined set of coordinates,
    adds it to the session, and commits it to the database. It then retrieves the object
    to ensure it was correctly saved and returns it for use in tests.

    Args:
        session: The SQLAlchemy session provided by the `session` fixture.
        crossection_no_layers: The Crossection object provided by the `crossection_no_layers` fixture.

    Returns:
        LocationInTopology: The created and committed LocationInTopology object.
    """
    from app.apps.dykes.models import LocationInTopology

    crossection = crossection_no_layers

    # Should only allow for two values X, Y, we use a list of two values
    # because using a dictionary makes things more complicated
    # For example this invalid coordinate would pass: {"x": 1, "y": 2, "x": 3}
    location = LocationInTopology(crossection_id=crossection.id, coordinates=[1, 2])
    session.add(location)
    session.commit()

    retrieved = session.query(LocationInTopology).filter_by(id=location.id).first()
    assert retrieved == location
    return retrieved


@pytest.fixture(scope="function")
def sensor(session, sensor_type):
    """
    Pytest fixture to create and commit a Sensor object.

    This fixture creates a Sensor object associated with a specific SensorType,
    adds it to the session, and commits it to the database. It then retrieves the object
    to ensure it was correctly saved and returns it for use in tests.

    Args:
        session: The SQLAlchemy session provided by the `session` fixture.
        sensor_type: The SensorType object provided by the `sensor_type` fixture.

    Returns:
        Sensor: The created and committed Sensor object.
    """
    from app.apps.dykes.models import Sensor

    sensor = Sensor(name="Test Sensor", sensor_type_id=sensor_type.id)
    session.add(sensor)
    session.commit()

    retrieved = session.query(Sensor).filter_by(id=sensor.id).first()
    assert retrieved == sensor
    return retrieved
