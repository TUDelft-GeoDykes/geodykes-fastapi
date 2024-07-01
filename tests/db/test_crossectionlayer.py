from conftest import generate_topologies


def test_create_crossection_layers(topology, dyke, crossection):
    from app.apps.dykes.models import Crossection, CrossectionLayer
    # Create a crossection

    assert crossection.id
    crossection.dyke_id = dyke.id
    assert crossection.dyke_id
    crosslayer = CrossectionLayer(crossection_id=crossection.id)
    assert crosslayer.crossection_id == crossection.id

