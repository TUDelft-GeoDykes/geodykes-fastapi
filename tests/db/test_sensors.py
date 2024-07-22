'''ACCEPTANCE CRITERIA
- Sensor types can be created
- Each reading has to be associated with a sensor type
- A sensor type has a name and details associated with it
- The name cannot be duplicated in the database
- If sensor is multisensor it must allow to have multiple units of measurement
- A sensor can be created in association with a sensor type and a location in a specific topology
'''
import pytest
from app.apps.dykes.models import SensorType, UnitOfMeasure, LocationInTopology, Sensor

# Sensor types must be created on demand
def test_create_sensor_type(session):
    sensor_type = SensorType(name='TempSensor', details='measures temperature')
    session.add(sensor_type)
    session.commit()

    # Verify sensor type is created
    assert sensor_type.id is not None
    assert sensor_type.name == 'TempSensor'
    assert sensor_type.details == 'measures temperature'

    # Try to create a duplicate sensor type
    duplicate_sensor_type = SensorType(name='TempSensor', details='measures temperature')

    with pytest.raises(Exception):
        session.add(duplicate_sensor_type)
        session.flush()

def test_add_units_to_sensor(session, unit_of_measure):
    # Test single sensor with one unit
    sensor_type_single = SensorType(name="SingleSensor", details="Single unit sensor", multisensor=False)
    sensor_type_single.units_of_measure.append(unit_of_measure)
    session.add(sensor_type_single)
    session.commit()

    assert len(sensor_type_single.units_of_measure) == 1

    # Test single sensor with multiple units (should fail)
    unit2 = UnitOfMeasure(unit="Fahrenheit", description="Temperature in Fahrenheit")
    session.add(unit2)
    session.commit()

    with pytest.raises(ValueError):
        sensor_type_single.units_of_measure.append(unit2)
        session.commit()

    # Test multisensor with multiple units
    sensor_type_multi = SensorType(name="MultiSensor", details="Multiple unit sensor", multisensor=True)
    sensor_type_multi.units_of_measure.append(unit_of_measure)
    sensor_type_multi.units_of_measure.append(unit2)
    session.add(sensor_type_multi)
    session.commit()

    assert len(sensor_type_multi.units_of_measure) == 2


def test_create_LocationInTopology(session, topology):
    location = LocationInTopology(topology_id=topology.id, coordinates=[1,2])
    session.add(location)
    session.commit()
    assert location.id is not None


# A sensor has to be associated with a sensor type and a location in a specific topology
def test_create_sensor(session, sensor_type, topology):
    location = LocationInTopology(topology_id=topology.id, coordinates=[1,2])
    sensor = Sensor(sensor_type=sensor_type, location=location, name="TempSensor")
    session.add(sensor)
    session.commit()
    assert sensor.id is not None
    assert sensor.sensor_type == sensor_type
    assert sensor.location == location