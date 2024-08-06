from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
import app.apps.dykes.models as models
from app.repositories.repository_interface import ReadingRepository

class DatabaseReadingRepository(ReadingRepository):
    """
    A repository class for accessing and manipulating readings in a database.

    This class provides methods for retrieving readings from the database, converting them to dictionaries,
    and performing asyncsynchronous retrieval of readings.

    Attributes:
        db (AsyncSession): The asynchronous database session used for querying the database.

    Methods:
        convert_to_dict: Converts a reading object to a dictionary format.
        get_all_readings: Retrieves all readings from the database asynchronously.
        sync_get_all_readings: Retrieves all readings from the database synchronously.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def convert_to_dict(self, obj):
        if not obj:
            return None
        return {
            "id": obj.id,
            "crossection": obj.crossection.name if obj.crossection else None,
            "location_in_topology": obj.location.coordinates if obj.location else None,
            "unit": obj.unit.unit if obj.unit else None,
            "value": obj.value,
            "time": obj.time.isoformat()
        }

    async def get_all_readings(self) -> List[models.Reading]:
        result = await self.db.execute(
            select(models.Reading)
            .options(
                selectinload(models.Reading.crossection),
                selectinload(models.Reading.location),
                selectinload(models.Reading.sensor),
                selectinload(models.Reading.unit)
            )
        )
        objects = result.scalars().all()
        items = [await self.convert_to_dict(obj) for obj in objects]
        return items
    
    def sync_get_all_readings(self) -> List[models.Reading]:
        pass

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