import json
import datetime

import pytest
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.apps.dykes.models import Topology

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
    topo = Topology(coordinates=TOPOLOGY_BASE_POINTS)
    session.add(topo)
    session.commit()

    retrieved = session.query(Topology).filter_by(id=topo.id).first()
    assert retrieved.coordinates == TOPOLOGY_BASE_POINTS
    return retrieved


# Helper function to generate topologies
def generate_topologies(num_topologies, y_distance) -> list:
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
    from app.apps.dykes.models import Dyke

    dyk = Dyke(name="test dyke", description="This is our testing dyke")

    session.add(dyk)
    session.commit()

    retrieved = session.query(Dyke).filter_by(id=dyk.id).first()
    assert retrieved == dyk

    return retrieved

# A simple crossection that with no layers
@pytest.fixture(scope="function")
def crossection_empty(session, dyke, topology):
    from app.apps.dykes.models import Crossection

    cross = Crossection(dyke_id=dyke.id, name="test crossection", 
                        description="empty description", topology=topology.id)

    session.add(cross)
    session.commit()

    retrieved = session.query(Crossection).filter_by(id=cross.id).first()
    assert retrieved == cross
    return retrieved


@pytest.fixture(scope="function")
def crossection(session, dyke, topologies):
    from app.apps.dykes.models import Crossection
    topology = topologies[0]
    cross = Crossection(dyke_id=dyke.id, name="test crossection", topology=topology.id)

    session.add(cross)
    session.commit()

    retrieved = session.query(Crossection).filter_by(id=cross.id).first()
    assert retrieved == cross
    return retrieved

# READING FIXTURES
@pytest.fixture(scope="function")
def timestamp():
    return datetime.datetime.strptime('26 Sep 2022', '%d %b %Y')

@pytest.fixture(scope="function")
def reading(session, crossection_empty, timestamp):
    from app.apps.dykes.models import Reading
    
    read = Reading(crossection_id=crossection_empty.id,
                   location_in_topology=1, unit="mm",value=10,
                   time=timestamp)
    session.add(read)
    session.commit()

    retrieved = session.query(Reading).filter_by(id=read.id).first()
    assert retrieved == read
    return retrieved