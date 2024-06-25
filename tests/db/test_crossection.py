def test_crossection_exists(session, crossection, dyke, topology):
    from app.apps.dykes.models import Dyke, Crossection

    retrieved = session.query(Crossection).filter_by(id=crossection.id).first()
    assert retrieved.name == "test crossection"