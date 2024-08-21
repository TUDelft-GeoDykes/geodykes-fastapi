"""
This script, schemas.py, serves as a central location for defining data validation and serialization schemas using Pydantic for the FastAPI application. These schemas are crucial for enforcing business rules and ensuring data integrity as information flows in and out of the application's endpoints.
"""
from datetime import datetime
from typing import List, Optional

import pydantic
from pydantic import BaseModel, Field, PositiveInt, ConfigDict

# Base class for all models, providing a common configuration setup using Pydantic's ConfigDict.
class Base(BaseModel):
    # Configuration to automatically use attributes from constructors for model instantiation.
    model_config = ConfigDict(from_attributes=True)

# DykeSchema serves as an abstract base class that defines common attributes and validations for all dyke models.
class DykeSchema(Base):
    """
    Abstract base class for dyke models, defining essential attributes and providing a foundation for more specific dyke models.
    It utilizes Python's inheritance mechanism to allow other models to extend this base class without duplicating common attributes.

    Attributes:
        name (str): Human-readable name of the dyke.
        description (Optional[str]): Detailed information about the dyke, if available.
    """
    name: str = Field(..., json_schema_extra={"example":"Duifpolder", "description":"The name of the dyke"})
    description: Optional[str] = Field(None, description="Additional information about the dyke")

# DykeCreate is designed for creating dyke records, inheriting common fields from DykeSchema and potentially adding more specific ones.
class DykeCreate(DykeSchema):
    pass

# Dykes is a container model for handling collections of Dyke instances, demonstrating aggregation of models in a list.
class Dykes(Base):
    items: List[DykeSchema]  # Aggregated list of Dyke instances, leveraging Pydantic's data validation for lists of complex models.

# TopologySchema defines a schema for topological structures with an id and a list of coordinates.
class TopologySchema(BaseModel):
    id: int
    coordinates: List[dict]

    model_config = ConfigDict(from_attributes=True)

# LocationInTopologySchema defines a schema for locations within a topology, using a list of coordinates.
class LocationInTopologySchema(BaseModel):
    coordinates: List[float]

    model_config = ConfigDict(from_attributes=True)

# CrossectionSchema defines a schema for crossections, linking them to a topology and a dyke.
class CrossectionSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    topology: str
    dyke: DykeSchema

    model_config = ConfigDict(from_attributes=True)

# UnitOfMeasureSchema defines a schema for units of measure with id, unit, and description.
class UnitOfMeasureSchema(BaseModel):
    id: int
    unit: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)

# SensorTypeSchema defines a schema for sensor types, with attributes such as id, name, details, and whether it is a multisensor.
class SensorTypeSchema(BaseModel):
    id: int
    name: str
    details: Optional[str]
    multisensor: bool

    model_config = ConfigDict(from_attributes=True)

# SensorSchema defines a schema for sensors, linking them to a location and sensor type.
class SensorSchema(BaseModel):
    id: int
    name: str
    sensor_type: str  # This can be a reference to a SensorTypeSchema
    location: List[float]  # This can be a reference to a LocationInTopologySchema
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

# Reading schema defines a structure for sensor readings, linking them to a crossection, sensor, and unit of measure.
class Reading(BaseModel):
    id: int  # Automatically generated
    crossection: str
    sensor_id: int
    sensor_name: str
    sensor_type: str
    sensor_is_active: bool
    location_in_topology: List[float]
    unit: str
    value: float
    time: datetime

    model_config = ConfigDict(from_attributes=True)

class ReadingCreate(BaseModel):
    crossection: str
    sensor_id: Optional[int]
    sensor_name: str
    sensor_is_active: bool
    location_in_topology: List[float]
    unit: str
    value: float
    time: datetime

    model_config = ConfigDict(from_attributes=True)


# Readings is a container model for handling collections of Reading instances.
class Readings(Base):
    readings: List[Reading]

# ReadingCreateUpdateSchema defines the schema for creating or updating sensor readings.
class ReadingCreateUpdateSchema(BaseModel):
    crossection_id: int
    location_in_topology_id: Optional[int]
    unit_id: int
    sensor_id: Optional[int]
    value: int
    time: datetime