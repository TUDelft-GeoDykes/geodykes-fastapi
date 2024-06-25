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

router = fastapi.APIRouter()

@router.get("/dykes/")
async def list_dykes() -> schemas.Dykes:
    # Fetch all dyke entries from the database using the Dyke model's all() method.
    objects = await models.Dyke.all()
    # Convert the list of Dyke model instances to Dykes schema for response.
    return typing.cast(schemas.Dykes, {"items": objects})

@router.get("/dykes/{dyke_id}/")
async def get_dyke(dyke_id: int) -> schemas.Dyke:
    # Retrieve a single Dyke by its ID, with prefetching related objects if necessary.
    instance = await models.Dyke.get_by_id(dyke_id, prefetch=('dykes',))
    # If no dyke is found, raise HTTP 404 error.
    if not instance:
        raise fastapi.HTTPException(status_code=404, detail="Dyke not found")
    # Serialize the Dyke model instance into Dyke schema and return.
    return typing.cast(schemas.Dyke, instance)
