import json

import pytest
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.orm import sessionmaker

from app.db.base import Base


@pytest.fixture(scope="session")
def engine():
    # Setup an engine connected to the in-memory or test database
    return create_engine("sqlite:///:memory:", echo=False)


@pytest.fixture(scope="session")
def tables(engine):
    # Create all tables in the database
    Base.metadata.create_all(engine)  # This creates all tables in the database
    return engine


@pytest.fixture(scope="session")
def inspector(engine):
    return reflection.Inspector.from_engine(
        engine
    )  # This we need to check that all tables are in the database


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


# TOPOLOGY FIXTURES


# Helper function to generate topologies
def generate_topologies(num_topologies, y_distance):
    topologies = []

    # Define the initial set of points for the first topology (surface of the earth)
    base_points = [
        {"x": 1, "y": 100},
        {"x": 2, "y": 200},
        {"x": 3, "y": 300},
        {"x": 4, "y": 400},
        {"x": 5, "y": 500},
        {"x": 6, "y": 600},
    ]

    for i in range(num_topologies):
        # Adjust the y-values for each subsequent topology
        points = [
            {"x": point["x"], "y": point["y"] - i * y_distance} for point in base_points
        ]
        topologies.append(points)

    return topologies


# This fixture allows to instantiate many topology data at once
@pytest.fixture(scope="session", params=generate_topologies(6, 50))
def topology_gen(request):
    return request.param


# With this fixture we use the topology data above to instantiate topology objects
# These is useful for example when creating a set of topologies to describe layers in a crossection
@pytest.fixture(scope="function")
def topologies(topology_gen, session):
    serialized = json.dumps(topology_gen)
    deserialized = json.loads(serialized)
    assert topology_gen == deserialized

    from app.apps.dykes.models import Topology

    topo = Topology(coordinates=topology_gen)

    session.add(topo)
    session.commit()

    retrieved = session.query(Topology).filter_by(id=topo.id).first()
    assert retrieved.coordinates == topology_gen

    return {"topology": retrieved}


# One single topology for simpler tests
@pytest.fixture(scope="function")
def topology(session):
    from app.apps.dykes.models import Topology

    coordinates = [
        {"x": 1, "y": 100},
        {"x": 2, "y": 200},
        {"x": 3, "y": 300},
        {"x": 4, "y": 400},
        {"x": 5, "y": 500},
        {"x": 6, "y": 600},
    ]

    topo = Topology(coordinates=coordinates)
    session.add(topo)
    session.commit()

    retrieved = session.query(Topology).filter_by(id=topo.id).first()
    assert retrieved.coordinates == topo.coordinates

    return retrieved


# DYKE FIXTURES
# Create a dyke fixture
@pytest.fixture(scope="function")
def dyke(session):
    from app.apps.dykes.models import Dyke

    dyk = Dyke(name="test dyke", description="This is our testing dyke")

    session.add(dyk)
    session.commit()

    retrieved = session.query(Dyke).filter_by(id=dyk.id).first()
    assert retrieved == dyk

    return retrieved


@pytest.fixture(scope="function")
def crossection(session, dyke, topology):
    from app.apps.dykes.models import Crossection

    cross = Crossection(dyke_id=dyke.id, name="test crossection", topology=topology.id)

    session.add(cross)
    session.commit()

    retrieved = session.query(Crossection).filter_by(id=cross.id).first()
    assert retrieved == cross
    return retrieved
