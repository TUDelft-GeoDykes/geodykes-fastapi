"""
This script defines the ORM models for the 'Dyke' and 'Crossection' entities using SQLAlchemy.
These models are central to the application's data layer, allowing for database interactions that support the creation, retrieval, update, and deletion of 'Dyke' and 'Crossection' records.
The models are used throughout the application, particularly in the controllers/views,
here they interact with the business logic to handle web requests and in the schemas for
validating and serializing data.
"""
import sqlalchemy as sa
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Table, ForeignKey, Integer, Column, Boolean, String
from app.db.models import BaseModel

# Dyke model represents the main structural entity, similar to the 'dyke' table in the schema.
class Dyke(BaseModel):
    __tablename__ = "dyke"  # Database table name
    name = sa.Column(sa.String, nullable=False)  # Name of the dyke
    description = sa.Column(sa.String, nullable=True)  # Optional detailed description of the dyke
    # Relationship to Crossection, indicating one dyke can have multiple crossections.
    crossections = relationship("Crossection", back_populates="dyke")

# Crossection model represents specific cross-sectional details of a dyke.
class Crossection(BaseModel):
    __tablename__ = "crossection"  # Database table name
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    dyke_id = sa.Column(sa.Integer, sa.ForeignKey("dyke.id"), nullable=False)  # Foreign key linking back to Dyke
    name = sa.Column(sa.String, nullable=False)  # Name or identifier of the crossection
    description = sa.Column(sa.String, nullable=True)  # Optional detailed description of the crossection
    topology = sa.Column(sa.String, nullable=False)  # Descriptive attribute for the shape or structure
    # Relationship to Timeseries, indicating one crossection can have multiple timeseries.
    timeseries = relationship("Reading", back_populates="crossection")
    crossection_layers = relationship("CrossectionLayer", back_populates="crossection")
    dyke = relationship("Dyke", back_populates="crossections")

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
    crossection_id = sa.Column(sa.Integer, sa.ForeignKey("crossection.id"), nullable=False)
    top_topology_id = sa.Column(sa.Integer, sa.ForeignKey("topology.id"), nullable=False)
    bottom_topology_id = sa.Column(sa.Integer, sa.ForeignKey("topology.id"), nullable=False)
    soil_type = sa.Column(sa.String, nullable=False)
    crossection = relationship("Crossection", back_populates="crossection_layers")
    top_topology = relationship("Topology", foreign_keys=[top_topology_id])
    bottom_topology = relationship("Topology", foreign_keys=[bottom_topology_id])

class LocationInTopology(BaseModel):
    '''This model represents a location in a topology. 
    It is used to store the coordinates of a location in a topology of a reading and sensor.
    '''
    __tablename__ = "location_in_topology"    
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    coordinates = sa.Column(sa.JSON, nullable=False) 
    topology_id = sa.Column(sa.Integer, sa.ForeignKey("topology.id"), nullable=False)

    def __repr__(self):
        return f"<LocationInTopologys(id={self.id}, coordinates={self.coordinates})>"

    # Should only allow for two values X, Y, we use a list of two values
    # because using a dictionary makes things more complicated
    # For example this invalid coordinate would pass: {"x": 1, "y": 2, "x": 3}
    @validates('coordinates')
    def validate_coordinates(self, key, value):
        if not isinstance(value, list) or len(value) != 2:
            raise ValueError("Coordinates must be a list of two values")
        return value
    
# Timeseries model is represented by timestamped readings
class Reading(BaseModel):
    __tablename__ = "reading"  # Database table name
    crossection_id = sa.Column(sa.Integer, sa.ForeignKey("crossection.id"), nullable=False)  # Foreign key linking back to Crossection
    # location_in_topology = sa.Column(sa.JSON, nullable=False)
    location_in_topology_id = sa.Column(sa.Integer, sa.ForeignKey("location_in_topology.id"), nullable=True) # This is inherited from the sensor location creating the reads
    unit_id = sa.Column(sa.Integer, sa.ForeignKey("unit_of_measure.id"), nullable=False)  # Foreign key linking to UnitOfMeasure
    sensor_type_id = sa.Column(sa.Integer, sa.ForeignKey("sensor_type.id"), nullable=True)
    value = sa.Column(sa.Integer, nullable=False)  # Value of the timeseries
    time = sa.Column(sa.DateTime, nullable=False)  # Timestamp for the reading
    crossection = relationship("Crossection", back_populates="timeseries")
    unit = relationship("UnitOfMeasure", backref="readings")
    location = relationship("LocationInTopology")


    def __repr__(self):
        return f"<Reading(crossection_id='{self.crossection_id}', location_in_topology='{self.location_in_topology}', unit_id='{self.unit_id}', value='{self.value}', time='{self.time}')>"
    
class SensorType(BaseModel):
    __tablename__ = 'sensor_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    details = Column(String, nullable=True)
    multisensor = Column(Boolean, default=False)
    
    units_of_measure = relationship('UnitOfMeasure', secondary='sensor_unit_association', cascade="all, delete")
    sensors = relationship('Sensor', back_populates='sensor_type')

    @validates('units_of_measure')
    def validate_units(self, key, unit):
        '''Validate the number of units for a multisensor type
        A single sensor type cannot have more than one unit of measure.'''
        if not self.multisensor and len(self.units_of_measure) >= 1:
            raise ValueError("Single sensor type cannot have more than one unit of measure.")
        return unit
    
class UnitOfMeasure(BaseModel):
    __tablename__ = 'unit_of_measure'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    unit = sa.Column(sa.String, nullable=False, unique=True)
    description = sa.Column(sa.String, nullable=True)

    def __repr__(self):
        return f"<UnitOfMeasure(unit='{self.unit}', description='{self.description}')>"

# Association table for the many-to-many relationship between SensorType and UnitOfMeasure
# A sensor type can measure multiple units, and a unit can be measured by multiple sensor types. 
sensor_unit_association = Table('sensor_unit_association', BaseModel.metadata,
    Column('sensor_type_id', Integer, ForeignKey('sensor_type.id'), primary_key=True),
    Column('unit_of_measure_id', Integer, ForeignKey('unit_of_measure.id'), primary_key=True)
)

class Sensor(BaseModel):
    ''' Sensors need to be monitored and managed, as it is common for them to fail and require maintenance or replacement.
    '''
    __tablename__ = "sensor"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    sensor_type_id = sa.Column(sa.Integer, sa.ForeignKey("sensor_type.id"), nullable=False)
    location_in_topology_id = sa.Column(sa.Integer, sa.ForeignKey("location_in_topology.id"), nullable=True)
    is_active = sa.Column(sa.Boolean, default=True)

    sensor_type = relationship("SensorType", back_populates="sensors")
    location = relationship("LocationInTopology")

    def __repr__(self):
        return f"<Sensor(id={self.id}, name={self.name}, sensor_type_id={self.sensor_type_id}, location_id={self.location_in_topology_id}, is_active={self.is_active})>"
