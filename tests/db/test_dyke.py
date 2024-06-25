# test that dyke is created
def test_dyke_exists(session, dyke):
    from app.apps.dykes.models import Dyke 

    retrieved = session.query(Dyke).filter_by(id=dyke.id).first()
    assert retrieved.name == "test dyke"