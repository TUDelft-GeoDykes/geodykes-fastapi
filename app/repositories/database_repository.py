from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.apps.dykes.models import Reading
from app.repositories.repository_interface import ReadingRepository

class DatabaseReadingRepository(ReadingRepository):
    '''
    '''
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

    async def get_all_readings(self) -> List[Reading]:
        result = await self.db.execute(
            select(Reading)
            .options(
                selectinload(Reading.crossection),
                selectinload(Reading.location),
                selectinload(Reading.sensor),
                selectinload(Reading.unit)
            )
        )
        objects = result.scalars().all()
        items = [await self.convert_to_dict(obj) for obj in objects]
        return items
    
    def sync_get_all_readings(self) -> List[Reading]:
        pass