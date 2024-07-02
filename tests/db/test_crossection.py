import pytest

# We need to use the parametrize decorator to pass the topologies fixture to the test, otherwise it will not be available
@pytest.mark.parametrize("topologies", [(1, 0)], indirect=True) 
def test_crossection_exists(session, crossection):
    from app.apps.dykes.models import Crossection

    retrieved = session.query(Crossection).filter_by(id=crossection.id).first()
    assert retrieved.name == "test crossection"