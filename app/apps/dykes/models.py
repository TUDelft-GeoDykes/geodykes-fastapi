"""
This script defines the ORM models for the 'Dyke' and 'Crossection' entities using SQLAlchemy.
These models are central to the application's data layer, allowing for database interactions that support the creation, retrieval, update, and deletion of 'Dyke' and 'Crossection' records.
The models are used throughout the application, particularly in the controllers/views,
here they interact with the business logic to handle web requests and in the schemas for
validating and serializing data.
"""
import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.models import BaseModel

# Dyke model represents the main structural entity, similar to the 'dyke' table in the schema.
class Dyke(BaseModel):
    __tablename__ = "dyke"  # Database table name
    dyke_id = sa.Column(sa.Integer, primary_key=True)  # Primary key, similar to 'id' in the database schema
    name = sa.Column(sa.String, nullable=False)  # Name of the dyke
    description = sa.Column(sa.String, nullable=True)  # Optional detailed description of the dyke
    # Relationship to Crossection, indicating one dyke can have multiple crossections.
    crossections = relationship("Crossection", backref="dyke")

# Crossection model represents specific cross-sectional details of a dyke.
class Crossection(BaseModel):
    __tablename__ = "crossection"  # Database table name
    crossection_id = sa.Column(sa.Integer, primary_key=True)  # Primary key, analogous to 'id' in the database schema
    dyke_id = sa.Column(sa.Integer, sa.ForeignKey("dyke.dyke_id"), nullable=False)  # Foreign key linking back to Dyke
    name = sa.Column(sa.String, nullable=False)  # Name or identifier of the crossection
    description = sa.Column(sa.String, nullable=True)  # Optional detailed description of the crossection
    topology = sa.Column(sa.String, nullable=False)  # Descriptive attribute for the shape or structure
    # Relationship to Timeseries, indicating one crossection can have multiple timeseries.
    timeseries = relationship("Timeseries", backref="crossection")

# Timeseries model represents timestampes of a certain unit
class Timeseries(BaseModel):
    __tablename__ = "timeseries"  # Database table name
    timeseries_id = sa.Column(sa.Integer, primary_key=True)  # Primary key, analogous to 'id' in the database schema
    crossection_id = sa.Column(sa.Integer, sa.ForeignKey("crossection.crossection_id"), nullable=False)  # Foreign key linking back to Crossection
    location_in_topology = sa.Column(sa.Integer, nullable=True)  # Location within the crossection
    unit = sa.Column(sa.String, nullable=True)  # Optional unit for the timeseries
    sensor_code = sa.Column(sa.Integer, nullable=False)  # A sensor's code of location within a measurement vertical
