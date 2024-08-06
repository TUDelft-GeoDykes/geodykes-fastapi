import app.apps.dykes.models as mo


def create_dyke(name, description=None):
    return mo.Dyke(name=name, description=description)

def create_crossection(dyke_id, name, description=None, topology=None):
    return mo.Crossection(dyke_id=dyke_id, name=name, description=description, topology=topology)


def create_topology(coordinates):
    return mo.Topology(coordinates=coordinates)


def create_crossection_layer(crossection_id, top_topology_id, bottom_topology_id, soil_type):
    return mo.CrossectionLayer(crossection_id=crossection_id, top_topology_id=top_topology_id, bottom_topology_id=bottom_topology_id, soil_type=soil_type)


def create_location_in_topology(coordinates, topology_id):
    return mo.LocationInTopology(coordinates=coordinates, topology_id=topology_id)


def create_reading(crossection_id, location_in_topology_id, unit_id, sensor_type_id, sensor_id, value, time):
    return mo.Reading(crossection_id=crossection_id, location_in_topology_id=location_in_topology_id, unit_id=unit_id, sensor_type_id=sensor_type_id, sensor_id=sensor_id, value=value, time=time)


def create_sensor_type(name, details=None, multisensor=False):
    return mo.SensorType(name=name, details=details, multisensor=multisensor)


def create_unit_of_measure(unit, description=None):
    return mo.UnitOfMeasure(unit=unit, description=description)
    

def create_sensor(name, sensor_type_id, location_in_topology_id=None, is_active=True):
    return mo.Sensor(name=name, sensor_type_id=sensor_type_id, location_in_topology_id=location_in_topology_id, is_active=is_active)
