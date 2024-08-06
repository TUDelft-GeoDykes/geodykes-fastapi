from app.factory.objects_factory import *

DYKES = [
    create_dyke(name="Dyke 1", description="description")
]

SENSORS = [
    create_sensor(name="Sensor 1", sensor_type_id=1),
    create_sensor(name="Sensor 2", sensor_type_id=1),
    create_sensor(name="Sensor 3", sensor_type_id=1)
]

READINGS = [
    create_reading(crossection_id=1, location_in_topology_id=1, unit_id=1, sensor_type_id=1, sensor_id=1, value=10, time="2022-01-01 12:00:00"),
    create_reading(crossection_id=1, location_in_topology_id=1, unit_id=1, sensor_type_id=1, sensor_id=1, value=20, time="2022-01-02 12:00:00"),
    create_reading(crossection_id=1, location_in_topology_id=1, unit_id=1, sensor_type_id=1, sensor_id=1, value=30, time="2022-01-03 12:00:00"),
    create_reading(crossection_id=1, location_in_topology_id=1, unit_id=1, sensor_type_id=1, sensor_id=2, value=15, time="2022-01-01 12:00:00"),
    create_reading(crossection_id=1, location_in_topology_id=1, unit_id=1, sensor_type_id=1, sensor_id=2, value=25, time="2022-01-02 12:00:00"),
    create_reading(crossection_id=1, location_in_topology_id=1, unit_id=1, sensor_type_id=1, sensor_id=2, value=35, time="2022-01-03 12:00:00"),
    create_reading(crossection_id=1, location_in_topology_id=1, unit_id=1, sensor_type_id=1, sensor_id=3, value=12, time="2022-01-01 12:00:00"),
    create_reading(crossection_id=1, location_in_topology_id=1, unit_id=1, sensor_type_id=1, sensor_id=3, value=22, time="2022-01-02 12:00:00"),
    create_reading(crossection_id=1, location_in_topology_id=1, unit_id=1, sensor_type_id=1, sensor_id=3, value=32, time="2022-01-03 12:00:00"),
    create_reading(crossection_id=1, location_in_topology_id=1, unit_id=1, sensor_type_id=1, sensor_id=4, value=18, time="2022-01-01 12:00:00"),
]

UNITS_OF_MEASURE = [
    create_unit_of_measure(unit="Unit 1"),
    create_unit_of_measure(unit="Unit 2")
]

TOPOLOGIES = [
    create_topology(coordinates="Coordinates 1"),
    create_topology(coordinates="Coordinates 2")
]
CROSSECTIONS = [
    create_crossection(dyke_id=1, name="Crossection 1", description="description", topology=1),
    create_crossection(dyke_id=1, name="Crossection 2", description="description", topology=2)
]

data = [DYKES, SENSORS, READINGS, UNITS_OF_MEASURE, TOPOLOGIES, CROSSECTIONS]