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
    name = sa.Column(sa.String, nullable=False)  # Name of the dyke
    description = sa.Column(sa.String, nullable=True)  # Optional detailed description of the dyke
    # Relationship to Crossection, indicating one dyke can have multiple crossections.
    crossections = relationship("Crossection", backref="dyke")

# Crossection model represents specific cross-sectional details of a dyke.
class Crossection(BaseModel):
    __tablename__ = "crossection"  # Database table name
    # crossection_id = sa.Column(sa.Integer, primary_key=True)  # Primary key, analogous to 'id' in the database schema
    dyke_id = sa.Column(sa.Integer, sa.ForeignKey("dyke.id"), nullable=False)  # Foreign key linking back to Dyke
    name = sa.Column(sa.String, nullable=False)  # Name or identifier of the crossection
    description = sa.Column(sa.String, nullable=True)  # Optional detailed description of the crossection
    topology = sa.Column(sa.String, nullable=False)  # Descriptive attribute for the shape or structure
    # Relationship to Timeseries, indicating one crossection can have multiple timeseries.
    timeseries = relationship("Timeseries", backref="crossection")
    crossection_layers = relationship("CrossectionLayer", backref="crossection")


class Topology(BaseModel):
    """
    Column to store coordinates in JSON format. This approach is chosen for several reasons:
    1. Data Integrity: Storing coordinates as a JSON array of objects (e.g., [{"x": 1, "y": 2}, {"x": 3, "y": 4}])
        ensures that each X and Y value is inherently paired, maintaining the structural integrity of coordinate data.
        data between a SQL database and a pandas DataFrame. This is particularly beneficial for data science and analytics
        workflows where pandas is a common tool for data manipulation.
    3. Database Performance: Using a JSON field leverages the capabilities of modern relational databases like PostgreSQL,
        which offer robust support for JSON, including functions and operators to manipulate JSON data and the ability to index JSON elements.
    4. Flexibility: JSON is a flexible data format that supports schema-less data structures. This allows for easy adjustments
        to the data model (like adding additional dimensions to coordinates) without altering the database schema.
    """
    __tablename__ = "topology"

    coordinates = sa.Column(sa.JSON)  # Example format: [{"x": 1, "y": 2}, {"x": 3, "y": 4}]

    # Additional methods and properties can be added here to facilitate operations like data validation,
    # manipulation of the JSON structure, or custom queries that leverage the JSON capabilities of the database.

class CrossectionLayer(BaseModel):
    """
    A layer is a 2D geometry composed of a top topology and a bottom topology. This model represents the layers of a crossection.
    """
    __tablename__ = "crossection_layer"
    # Crossection id to which the layer belongs
    crossection_id = sa.Column(sa.Integer, sa.ForeignKey("crossection.id"), nullable=False)
    # A reference later which is the topology on top that defines the layer
    top_topology_id = sa.Column(sa.Integer, sa.ForeignKey("topology.id"), nullable=False)
    # A reference later which is the topology on bottom that defines the layer
    bottom_topology_id = sa.Column(sa.Integer, sa.ForeignKey("topology.id"), nullable=False)
    soil_type = sa.Column(sa.String, nullable=False)


# Timeseries model represents timestampes of a certain unit
class Timeseries(BaseModel):
    __tablename__ = "timeseries"  # Database table name
    timeseries_id = sa.Column(sa.Integer, primary_key=True)  # Primary key, analogous to 'id' in the database schema
    crossection_id = sa.Column(sa.Integer, sa.ForeignKey("crossection.id"), nullable=False)  # Foreign key linking back to Crossection
    location_in_topology = sa.Column(sa.Integer, nullable=True)  # Location within the crossection
    unit = sa.Column(sa.String, nullable=True)  # Optional unit for the timeseries
    sensor_code = sa.Column(sa.Integer, nullable=False)  # A sensor's code of location within a measurement vertical
