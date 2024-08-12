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
            "sensor_location": location_coordinates,
            "sensor_is_active": obj.sensor.is_active if obj.sensor else None,
            "location_in_topology": obj.location.coordinates if obj.location else None,
            "unit": obj.unit.unit if obj.unit else None,
            "value": obj.value,
            "time": obj.time.isoformat(),
        }

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

    async def create_reading(self, payload) -> models.Reading:
        print("Creating reading")
        print(f"Payload is: {payload}")
        print(f"Payload type is: {type(payload)}")

        # We need to identify the topology first, the topology is from a crossection
        crossection_query = await self.db.execute(
            select(models.Crossection)
            .where(models.Crossection.name == payload.crossection)
        )
        crossection = crossection_query.scalars().first()
        if not crossection:
            raise ValueError("Crossection not found")
        
        topology_str = crossection.topology
        print(f"Topology string is: {topology_str}")

        # The topology str in the crossection should be a valid set of coordinates
        # If topology does not have a valid set of coordinaters, replace it with a valid set
        

        # try:
        #     topology =  await self.db.execute(
        #         select(models.Topology)
        #         .where(models.Topology.coordinates == topology_str)
        #     )
        #     print(f"Topology is: {topology}")
        # except ValueError:
        #     raise ValueError("Topology not found")
    
        # Now we create the location for the reading in the topology of the crossection
        # location = models.LocationInTopology(coordinates=payload.location_in_topology, 
        #                                      topology_id=topology)
        # print(f"Location is: {location}")
        # Get sensor type id from the sensor
        # sensor_type = await db.execute(select(models.SensorType).where(models.SensorType.name == "SensorType 1"))
        # As an option get the sensor id from the sensor name (which is supposed to be unique)

        # Create a reading instance
        # data = data.dict()
        # data["unit_id"] = unit
        # data["crossection_id"] = crossection
        # data["sensor_type_id"] = sensor_type
        # data["location_in_topology_id"] = location

        # print("DEBUG")
        # print(data)
        # instance = await models.Reading(**data)
        # print(instance)
        # return instance

        # try:
        #     instance = await models.Reading(**data.dict())
        #     print("DEBUG")
        #     print(instance)
        # except Exception:
        #     raise Exception

        # return instance
        # return typing.cast(schemas.Reading, instance)

        return "Created"