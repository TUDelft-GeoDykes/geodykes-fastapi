"""
This script, schemas.py, serves as a central location for defining data validation and serialization schemas using Pydantic for the FastAPI application. These schemas are crucial for enforcing business rules and ensuring data integrity as information flows in and out of the application's endpoints.

"""
from datetime import datetime
from typing import List, Optional

import pydantic
from typing import Optional
from pydantic import BaseModel, Field, PositiveInt

# Base class for all models, providing a common configuration setup using Pydantic's ConfigDict.
class Base(BaseModel):
    # Configuration to automatically use attributes from constructors for model instantiation.
    model_config = pydantic.ConfigDict(from_attributes=True)

# DykeBase serves as an abstract base class that defines common attributes and validations for all dyke models.
class DykeSchema(Base):
    """
    Abstract base class for dyke models, defining essential attributes and providing a foundation for more specific dyke models.
    It utilizes Python's inheritance mechanism to allow other models to extend this base class without duplicating common attributes.

    Attributes:
        name (str): Human-readable name of the dyke.
        description (Optional[str]): Detailed information about the dyke, if available.
    """
    name: str = Field(..., example="Duifpolder", description="The name of the dyke")
    description: Optional[str] = Field(None, description="Additional information about the dyke")

# DykeCreate is designed for creating dyke records, inheriting common fields from DykeBase and potentially adding more specific ones.
class DykeCreate(DykeSchema):
    pass

# Dyke model includes a unique identifier and extends DykeBase, showcasing how inheritance can add additional properties to a base configuration.
# class Dyke(DykeBase):
#     dyke_id: PositiveInt | None = None  # Unique identifier for the dyke, added to the basic structure provided by DykeBase.

# Dykes is a container model for handling collections of Dyke instances, demonstrating aggregation of models in a list.
class Dykes(Base):
    items: list[DykeSchema]  # Aggregated list of Dyke instances, leveraging Pydantic's data validation for lists of complex models.


class TopologySchema(BaseModel):
    id: int
    coordinates: List[dict]

    class Config:
        from_attributes = True


class LocationInTopologySchema(BaseModel):
    # id: int
    coordinates: List[float]
    # topology: TopologySchema

    class Config:
        from_attributes = True


class CrossectionSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    topology: str
    dyke: DykeSchema

    class Config:
        from_attributes = True


class UnitOfMeasureSchema(BaseModel):
    id: int
    unit: str
    description: Optional[str]

    class Config:
        from_attributes = True


class SensorTypeSchema(BaseModel):
    id: int
    name: str
    details: Optional[str]
    multisensor: bool

    class Config:
        from_attributes = True


class SensorSchema(BaseModel):
    id: int
    name: str
    sensor_type: str # SensorTypeSchema
    location: List[float] #LocationInTopologySchema
    is_active: bool

    class Config:
        from_attributes = True

class Reading(BaseModel):
    id: int  # Automatically generated
    crossection: str
    sensor_id: int
    sensor_name: str
    sensor_type: str
    sensor_location: List[float]
    sensor_is_active: bool
    location_in_topology: List[float]
    unit: str
    value: float
    time: datetime

    class Config:
        from_attributes = True


class Readings(Base):
    readings: list[Reading]

# For creating or updating readings
class ReadingCreateUpdateSchema(BaseModel):
    crossection_id: int
    location_in_topology_id: Optional[int]
    unit_id: int
    sensor_id: Optional[int]
    value: int
    time: datetime