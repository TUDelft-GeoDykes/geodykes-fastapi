from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from typing import List, Type, TypeVar, Optional, Dict
import app.apps.dykes.models as models
from app.repositories.repository_interface import ReadingRepository

# Define a generic type variable 'T'
# This allows us to write functions that can operate on any type of model
T = TypeVar('T')


class DatabaseReadingRepository(ReadingRepository):
    """
    A repository class for accessing and manipulating readings in a database.

    This class provides methods for retrieving readings from the database, converting them to dictionaries,
    and performing asyncsynchronous retrieval of readings.

    Attributes:
        db (AsyncSession): The asynchronous database session used for querying the database.

    Methods:
        convert_to_dict: Converts a reading object to a dictionary format.
        get_readings: Retrieves all readings from the database asynchronously.
        sync_get_readings: Retrieves all readings from the database synchronously.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def fetch_related_model(self, model: Type[T], model_id: int) -> Optional[T]:
        """
        Fetch a related model by its ID.

        Args:
            model (Type[T]): The model class to query. This can be any SQLAlchemy model class.
            model_id (int): The ID of the model instance to fetch.

        Returns:
            Optional[T]: The fetched model instance or None if not found.

        The purpose of this function is to abstract the logic of fetching related models,
        making the code more reusable and easier to maintain.
        """
        result = await self.db.execute(
            select(model)
            .where(model.id == model_id)
        )
        return result.scalar()
    
    async def convert_to_dict(self, obj):
        if not obj:
            return None
        
        # Fetch related models using the generic function
        sensor_type = await self.fetch_related_model(models.SensorType, obj.sensor.sensor_type_id)
        location = await self.fetch_related_model(models.LocationInTopology, obj.sensor.location_in_topology_id)
        
        # Flatten the sensor details into the reading dictionary
        sensor_type_name = sensor_type.name if sensor_type else None
        location_coordinates = location.coordinates if location else None

        return {
            "id": obj.id,
            "crossection": obj.crossection.name if obj.crossection else None,
            "sensor_id": obj.sensor.id if obj.sensor else None,
            "sensor_name": obj.sensor.name if obj.sensor else None,
            "sensor_type": sensor_type_name,
            "sensor_is_active": obj.sensor.is_active if obj.sensor else None,
            "location_in_topology": obj.location.coordinates if obj.location else None,
            "unit": obj.unit.unit if obj.unit else None,
            "value": obj.value,
            "time": obj.time.isoformat(),
        }

    async def _get_reading(self, reading_id: int) -> Optional[models.Reading]:
        pass

    async def get_readings(self, start_date: Optional[datetime] = None,
                                end_date: Optional[datetime] = None,
                                sensor_ids: Optional[List[int]] = None,
                                sensor_names: Optional[List[str]] = None) -> List[dict]:
        query = select(models.Reading).options(
            # WHY SELECTINLOAD?
            # Queries using SQLAlchemy are constructed different depending on the load strategy used.
            # For example, selectinload or joinedload.
            # Generates multiple, smaller queries.
            # Can be more efficient if the related objects are highly distinct or if the main table has many rows.
            # Reduces the amount of redundant data transferred, which can be beneficial when fetching large datasets.

            selectinload(models.Reading.crossection),
            selectinload(models.Reading.location),
            # We make this query because currently we don't have too much data in the database
            # However in a context of larger datasets selectinload can be a better option
            joinedload(models.Reading.sensor).joinedload(models.Sensor.sensor_type),
            selectinload(models.Reading.unit)
        )

        if start_date and end_date:
            query = query.filter(models.Reading.time.between(start_date, end_date))
        elif start_date:
            query = query.filter(models.Reading.time >= start_date)
        elif end_date:
            query = query.filter(models.Reading.time <= end_date)
        if sensor_ids:
            query = query.where(models.Reading.sensor_id.in_(sensor_ids))
        elif sensor_names:
            # Remove any leading or trailing whitespace or quotes to avoid issues with the query
            sensor_names = [sensor_name.strip().strip('"') for sensor_name in sensor_names]
            query = query.join(models.Sensor).where(models.Sensor.name.in_(sensor_names))

        result = await self.db.execute(query)
        objects = result.scalars().all()
        readings = [await self.convert_to_dict(obj) for obj in objects]
        return readings

    # Query to fetch sensor, its type, and the associated units of measure
    async def get_sensor_with_units(self, db_session, sensor_name):
        query = (
            select(models.Sensor)
            .options(
                joinedload(models.Sensor.sensor_type).joinedload(models.SensorType.units_of_measure)
            )
            .where(models.Sensor.name == sensor_name)
        )

        result = await db_session.execute(query)
        sensor = result.scalars().first()

        if sensor:
            return {
                "sensor": sensor,
                "sensor_type": sensor.sensor_type,
                "units_of_measure": sensor.sensor_type.units_of_measure
            }
        else:
            print("Sensor not found")
            return None

    async def create_reading(self, payload) -> models.Reading:
        # Identify the crossection first
        crossection_query = await self.db.execute(
            select(models.Crossection)
            .where(models.Crossection.name == payload.crossection)
        )
        crossection = crossection_query.scalars().first()
        if not crossection:
            raise ValueError("Crossection not found")

        # Create or retrieve the location in the topology
        location = models.LocationInTopology(coordinates=payload.location_in_topology,
                                            crossection_id=crossection.id)

        # Save the location to the database
        self.db.add(location)
        await self.db.flush()  # Ensure the location ID is generated

        # Get sensor and its associated units using the helper function
        sensor_data = await self.get_sensor_with_units(self.db, payload.sensor_name)
        if not sensor_data:
            raise ValueError("Sensor not found")
        
        sensor = sensor_data['sensor']
        sensor_type = sensor_data['sensor_type']
        sensor_units = sensor_data['units_of_measure'][0] # Assuming the first unit is the default

        # Create the reading instance
        reading = models.Reading(
            crossection_id=crossection.id,
            location_in_topology_id=location.id,
            unit_id=sensor_units.id,  # Set the unit ID based on the sensor's sensor type
            sensor_type_id=sensor_type.id,
            sensor_id=sensor.id,
            value=payload.value,
            time=payload.time
        )

        # Add and commit the reading to the database
        self.db.add(reading)
        await self.db.commit()
        await self.db.refresh(reading)  # Refresh to get any generated values like ID

        # Fetch the reading from the database
        query = select(models.Reading).where(models.Reading.id == reading.id)
        result = await self.db.execute(query)
        reading = result.scalar()
        
        # return reading as a dictionary to be validated 
        return await self.convert_to_dict(reading)
