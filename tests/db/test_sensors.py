'''ACCEPTANCE CRITERIA
- Sensor types can be created
- Each reading has to be associated with a sensor type
- A sensor type has a name and details associated with it
- The name cannot be duplicated in the database
- If sensor is multisensor it must allow to have multiple units of measurement
'''
import pytest

def test_create_sensor_type(session, unit_of_measure):
    from app.apps.dykes.models import SensorType
    
    sensor_type = SensorType(name='X40', details='A sensor to measure temperature')
                            #  , unit_of_measure=unit_of_measure, multisensor=False)
    session.add(sensor_type)
    session.commit()

    # With pytest raise error because a sensory type name needs to be unique
    duplicate_sensor_type = SensorType(name='X40', details='A sensor to measure temperature')

    with pytest.raises(Exception):
        session.add(duplicate_sensor_type)
        session.flush()

# def 




   