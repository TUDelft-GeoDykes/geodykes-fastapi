"""
Roles and Relationships:
- schemas.py (This script): Defines data transfer objects (DTOs) that are used throughout the application 
  to validate and serialize data received from or sent to clients. It ensures that data adheres to 
  expected formats and types, leveraging Pydantic's powerful validation capabilities.

- models.py (SQLAlchemy models): Contains the SQLAlchemy ORM models that map directly to database tables. 
  These models are responsible for database operations and reflect the application's data structure 
  at the database level. The models defined in models.py often have a one-to-one correspondence to the 
  schemas defined in this script, but they include additional SQLAlchemy-specific configurations and 
  methods for database interactions.

- controllers or views (Typically routes in FastAPI): Utilize schemas defined in this script to validate 
  incoming data, serialize outgoing data, and handle HTTP request and response logic. Controllers fetch 
  and manipulate data through models but communicate with clients by serializing models to schemas or 
  deserializing request data to schemas before processing. This ensures that data is correctly typed and 
  structured before any business logic is applied.

For example, when a POST request is made to create a new dyke, the controller will:
1. Deserialize the incoming JSON payload to a DykeCreate schema instance to validate the data.
2. Convert the validated DykeCreate schema instance to a SQLAlchemy model instance.
3. Persist the new model instance to the database using operations defined in models.py.
4. Serialize the newly created model back to a Dyke schema instance to prepare the response.

This layered approach ensures a clear separation of concerns where:
- `schemas.py` handles data validation and serialization.
- `models.py` manages database interactions.
- Controllers orchestrate the flow between user inputs and backend responses, providing a clean interface 
  for data manipulation and presentation.
"""

import typing
import fastapi
from app.apps.dykes import models, schemas

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.db.deps import get_db

from app.repositories.repository_interface import ReadingRepository
from app.dependencies import get_reading_repository

router = fastapi.APIRouter()

@router.get("/dykes/")
async def list_dykes() -> schemas.Dykes:
    # Fetch all dyke entries from the database using the Dyke model's all() method.
    objects = await models.Dyke.all()
    return typing.cast(schemas.Dykes, {"items": objects[:2]})

@router.get("/dykes/{dyke_id}/")
async def get_dyke(dyke_id: int) -> schemas.DykeSchema:
    # Retrieve a single Dyke by its ID, with prefetching related objects if necessary.
    instance = await models.Dyke.get_by_id(dyke_id, prefetch=('dykes',))
    # If no dyke is found, raise HTTP 404 error.
    if not instance:
        raise fastapi.HTTPException(status_code=404, detail="Dyke not found")
    # Serialize the Dyke model instance into Dyke schema and return.
    return typing.cast(schemas.DykeSchema, instance)


async def list_readings(repository: ReadingRepository = Depends(get_reading_repository)):
    objects = await repository.get_all_readings()

    if not objects:
        raise HTTPException(status_code=404, detail="No readings found")
    
    # Convert ORM objects to dictionary representation
    def convert_to_dict(obj):
        if not obj:
            return None
        return {
            "id": obj.id,
            "crossection": obj.crossection and obj.crossection.name,
            "location_in_topology": obj.location and obj.location.coordinates,
            "unit": obj.unit and obj.unit.unit,
            "value": obj.value,
            "time": obj.time.isoformat()
        }
    
    items = [convert_to_dict(obj) for obj in objects]

    if not objects:
        raise HTTPException(status_code=404, detail="No readings found")
    
    # Return validated readings schema
    return schemas.Readings(items=items)
   
@router.post("/readings/", response_class=JSONResponse)
async def create_readings():
    ''' A prototype for this endpoint testing the main concept
    USE CASE:
    A user provides a csv file with readings, or python loaded dictionaries with readings
    (I am assuming csv is more appropriate for this case)
    The user also needs to provide a header to the endpoint that identifies:
    - The metadata should have the following fields:
    - The sensor this data is coming from
    - The sensor should be related to an id in the database
    - Alternatively the user can create a new sensor first.
    - If the following fields are not provided, the endpoint should return an error.


    USE CASE B:
    - The user has a csv file and list where there are different sensors
    - The name of the sensor is used to identify the sensor and perform the check
    - How it should work: The file is uploaded, the endpoint reads the file and checks the sensor name
       - Use yield to iterate over the file and check the sensor name


    '''
    # Validate the data (This is a cascade of validations)
    # The session should be opened for a while to ask the user several questions
    # The simplest algorithm is that the sensor must exist in order to create a reading
    # This is a more advanced version of validation and creation of readings we don't need right away
    # Check if sensor exists
        # If not create a new sensor
            # Check if crossection exists
                # If not create a new crossection
                    # Check if dyke exists if not create a dyke
    
    pass

# @router.post("/readings/", response_class=JSONResponse)
# async def create_readings(readings: List[schemas.ReadingCreate], db: AsyncSession = Depends(get_db)):
#     '''This is the description of the concept of this endpoint
    
#     '''
    
    
#     # Create a list to store the created reading instances
#     created_readings = []
    
#     # Iterate over each reading in the batch
#     for reading in readings:
#         # Check if the crossection exists
#         crossection = await models.Crossection.get_by_id(reading.crossection_id)
#         if not crossection:
#             raise HTTPException(status_code=404, detail="Crossection not found")
        
#         # Check if the dyke exists
#         dyke = await models.Dyke.get_by_id(reading.dyke_id)
#         if not dyke:
#             raise HTTPException(status_code=404, detail="Dyke not found")
        
#         # Check if the sensor exists
#         sensor = await models.Sensor.get_by_id(reading.sensor_id)
#         if not sensor:
#             raise HTTPException(status_code=404, detail="Sensor not found")
        
#         # Create the reading instance
#         reading_instance = models.Reading(
#             crossection_id=reading.crossection_id,
#             dyke_id=reading.dyke_id,
#             sensor_id=reading.sensor_id,
#             value=reading.value,
#             time=reading.time
#         )
        
#         # Add the reading instance to the session
#         db.add(reading_instance)
        
#         # Append the reading instance to the created_readings list
#         created_readings.append(reading_instance)
    
#     # Commit the session to persist the created readings
#     await db.commit()
    
#     # Convert the created readings to dictionary representation
#     def convert_to_dict(reading):
#         return {
#             "id": reading.id,
#             "crossection": reading.crossection and reading.crossection.name,
#             "dyke": reading.dyke and reading.dyke.name,
#             "sensor": reading.sensor and reading.sensor.name,
#             "value": reading.value,
#             "time": reading.time.isoformat()
#         }
    
#     # Convert the created readings to dictionary representation
#     created_readings_dict = [convert_to_dict(reading) for reading in created_readings]
    
#     # Return the created readings
#     return schemas.Readings(items=created_readings_dict)