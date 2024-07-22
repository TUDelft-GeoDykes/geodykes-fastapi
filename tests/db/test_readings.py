''' ACCEPTANCE CRITERIA FOR READINGS
- A reading is timestamped and has a value
- A reading cannot be created without a reference to a cross section
- A reading cannot be created without a value
- A reading cannot be created without a location
- A reading cannot be created without a unit
- A reading might not be created without a sensor
'''
import pytest
from sqlalchemy.exc import IntegrityError

def test_bad_reading(crossection_empty, session):
    from app.apps.dykes.models import Reading
    
    # Raise pytest errors
    with pytest.raises (IntegrityError): 
        wrong_read = Reading()
        session.add(wrong_read)
        session.flush() # Force the flush to the database to raise the error

# UnitsOfMeasure need to be defined before we create a reading
def test_create_unit_of_measure(session):
    from app.apps.dykes.models import UnitOfMeasure

    unit = UnitOfMeasure(unit="pressure", description="Description of this unit of measure")
    
    session.add(unit)
    session.commit()

    retrieved = session.query(UnitOfMeasure).filter_by(id=unit.id).first()
    assert retrieved == unit
    return retrieved

# A reading will have an id and a relation to a specific crossection
def test_create_reading(crossection_empty, session, timestamp, unit_of_measure, sensor_type, location_in_topology):
    from app.apps.dykes.models import Reading

    assert isinstance(crossection_empty.timeseries, list)
    assert crossection_empty.timeseries == [] # Check if the list of timeseries is empty

    read = Reading(crossection_id=crossection_empty.id,
                   location_in_topology_id=location_in_topology.id, unit_id=unit_of_measure.id,
                   sensor_type_id=sensor_type.id,
                   value=10, time=timestamp)
    
    session.add(read)
    session.commit()
    assert crossection_empty.timeseries

# Write a test to validate this line from the LocationInTopology model
def test_location_in_topology_coordinates(session, topology):
    from app.apps.dykes.models import LocationInTopology 

    # Test case 1: Valid coordinates
    valid_coordinates = [1, 2]
    location = LocationInTopology(topology_id=topology.id, coordinates=valid_coordinates)
    session.add(location)
    session.commit()
    assert location.id is not None

    # Test case 2: Invalid coordinates (more than 2 values)
    invalid_coordinates = [1, 2, 3]
    with pytest.raises(ValueError):
        location = LocationInTopology(topology_id=topology.id, coordinates=invalid_coordinates)
        session.add(location)
        session.commit()

    # Test case 3: Invalid coordinates (less than 2 values)
    invalid_coordinates = [1]
    with pytest.raises(ValueError):
        location = LocationInTopology(topology_id=topology.id, coordinates=invalid_coordinates)
        session.add(location)
        session.commit()
