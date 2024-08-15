import pytest
from app.apps.dykes.models import Dyke

def test_dyke_exists(session, dyke):
    retrieved = session.query(Dyke).filter_by(id=dyke.id).first()
    assert retrieved.name == "test dyke"

# test that a crossection name is unique
# @pytest.mark.parametrize("topologies", [(1, 0)], indirect=True)
def test_no_dyke_duplicates(session, dyke):
    dyke_name = dyke.name
    assert isinstance(dyke_name, str)
    assert dyke_name is not None
    duplicate = Dyke(name=dyke_name, description="Another description")
    with pytest.raises(Exception):
        session.add(duplicate)
        session.commit()