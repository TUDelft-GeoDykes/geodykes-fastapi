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

# A reading will have an id and a relation to a specific crossection
def test_create_reading(crossection_empty, session, timestamp):
    from app.apps.dykes.models import Reading

    assert isinstance(crossection_empty.timeseries, list)
    assert crossection_empty.timeseries == [] # Check if the list of timeseries is empty

    read = Reading(crossection_id=crossection_empty.id,
                   location_in_topology={"x": 1, "y": 100}, unit="mm",value=10,
                   time=timestamp)
    
    session.add(read)
    session.commit()
    assert crossection_empty.timeseries

# def test_create_unit_of_measure(session):
#     from app.apps.dykes.models import UnitOfMeasure

#     unit = UnitOfMeasure(unit="pressure", description="Description of this unit of measure")
    
#     session.add(unit)
#     session.commit()

#     retrieved = session.query(UnitOfMeasure).filter_by(id=unit.id).first()
#     assert retrieved == unit
#     return retrieved