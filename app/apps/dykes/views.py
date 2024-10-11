"""Roles and Relationships:
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
from datetime import datetime

import fastapi
from fastapi import Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.apps.dykes import models, schemas
from app.dependencies import get_reading_repository
from app.repositories.repository_interface import ReadingRepository


router = fastapi.APIRouter()


@router.get("/dykes/")
async def list_dykes() -> schemas.Dykes:
    # Fetch all dyke entries from the database using the Dyke model's all() method.
    objects = await models.Dyke.all()
    return typing.cast(schemas.Dykes, {"items": objects})


@router.get("/dykes/{dyke_id}/")
async def get_dyke(dyke_id: int) -> schemas.DykeSchema:
    # Retrieve a single Dyke by its ID, with prefetching related objects if necessary.
    instance = await models.Dyke.get_by_id(dyke_id, prefetch=("dykes"))
    # If no dyke is found, raise HTTP 404 error.
    if not instance:
        raise fastapi.HTTPException(status_code=404, detail="Dyke not found")
    # Serialize the Dyke model instance into Dyke schema and return.
    return typing.cast(schemas.DykeSchema, instance)


@router.get("/readings/", response_class=JSONResponse)
async def list_readings(
    start_date: datetime | None = Query(None, alias="startDate"),
    end_date: datetime | None = Query(None, alias="endDate"),
    sensor_ids: list[int] | None = Query(None, alias="sensorId"),
    sensor_names: list[str] | None = Query(None, alias="sensorName"),
    repository: ReadingRepository = Depends(get_reading_repository),
) -> schemas.Readings:
    """Retrieve readings from the database asynchronously.
    The user should be able to filter readings by start date, end date, and sensor ID.
    These parameters are optional and should allow to flexible query different subsets of readings.

    Args:
        start_date (Optional[datetime]): The start date to filter readings by.
        end_date (Optional[datetime]): The end date to filter readings by.
        sensor_id (Optional[int]): The sensor ID to filter readings by.
        sensor_name (Optional[str]): The sensor name to filter readings by.

    """
    objects = await repository.get_readings(start_date=start_date,
                                            end_date=end_date,
                                            sensor_ids=sensor_ids,
                                            sensor_names=sensor_names)
    if not objects:
        raise HTTPException(status_code=404, detail="No readings found")

    # Validate objects coming from repository
    try:
        validated_objects = schemas.Readings(readings=objects)
    except ValidationError:
        raise HTTPException(status_code=500, detail="Data validation error")

    return validated_objects


@router.post("/readings/", response_model=schemas.Reading, status_code=status.HTTP_201_CREATED)
async def create_reading(
    payload: schemas.ReadingCreate,
    repository: ReadingRepository = Depends(get_reading_repository),
    ):
    # return "Valid payload submitted"
    objects = await repository.create_reading(payload)

    if not objects:
        raise HTTPException(status_code=404)

    # Validate objects coming from repository
    try:
        validated_objects = schemas.Reading(**objects)
    except ValidationError:
        raise HTTPException(status_code=500, detail="Data validation error")

    return validated_objects
