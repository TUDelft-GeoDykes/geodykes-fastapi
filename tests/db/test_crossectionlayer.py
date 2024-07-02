import pytest

@pytest.mark.parametrize("topologies",[(2, 30)], indirect=True)
def test_create_crossection_layer(dyke, crossection, topologies):
    from app.apps.dykes.models import CrossectionLayer
    assert crossection.id
    crossection.dyke_id = dyke.id
    assert crossection.dyke_id
    crosslayer = CrossectionLayer(crossection_id=crossection.id)
    assert crosslayer.crossection_id == crossection.id
    
    crosslayer.top_topology_id = topologies[0].id
    assert crosslayer.top_topology_id
    assert crosslayer.top_topology_id == topologies[0].id

    crosslayer.bottom_topology_id = topologies[1].id
    assert crosslayer.bottom_topology_id
    assert crosslayer.top_topology_id == topologies[0].id

# Now we want to test that A section can have multiple crossection layers

