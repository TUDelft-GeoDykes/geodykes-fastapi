import pytest
from app.apps.dykes.models import Crossection

# We need to use the parametrize decorator to pass the topologies fixture to the test, otherwise it will not be available
@pytest.mark.parametrize("topologies", [(1, 0)], indirect=True) 
def test_crossection_exists(session, crossection):

    retrieved = session.query(Crossection).filter_by(id=crossection.id).first()
    assert retrieved.name == "test crossection"

# test that a crossection name is unique
@pytest.mark.parametrize("topologies", [(1, 0)], indirect=True) 
def test_no_crossection_duplicates(session, dyke, crossection, topology):
    crossection_name = crossection.name
    assert isinstance(crossection_name, str) 
    assert crossection_name is not None
    duplicate = Crossection(dyke=dyke, name=crossection_name, topology=topology.coordinates)
    with pytest.raises(Exception):
        session.add(duplicate)
        session.commit()