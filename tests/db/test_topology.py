
# test_topology.py
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
