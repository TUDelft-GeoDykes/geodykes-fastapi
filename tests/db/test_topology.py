import pytest

def test_add_topology(session):
    from app.apps.dykes.models import Topology
    # Assuming that Topology has been imported from models.models
    topo = Topology(coordinates=[{"x": 10, "y": 20}, {"x": 15, "y": 25}])

    session.add(topo)
    session.commit()

    retrieved = session.query(Topology).first()
    assert retrieved.coordinates == [{"x": 10, "y": 20}, {"x": 15, "y": 25}]

def test_empty_coordinates(session):
    from app.apps.dykes.models import Topology
    topo = Topology(coordinates=[])
    session.add(topo)
    session.commit()

    retrieved = session.query(Topology).first()
    assert retrieved.coordinates == []

# Test topologies generation using dynamic fixtures 
@pytest.mark.parametrize("topologies", [
    (3, 30),  # 3 topologies with y-distance of 30
    (5, 50),  # 5 topologies with y-distance of 50
    (6, 10)   # 6 topologies with y-distance of 10
], indirect=True)
def test_topologies(topologies):
    assert len(topologies) > 0  # Check if there are any topologies generated
    for topology in topologies:
        assert len(topology.coordinates) == 6  # Ensure each topology has 6 points
        for point in topology.coordinates:
            assert "x" in point and "y" in point  # Ensure each point has x and y coordinates