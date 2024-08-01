from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.apps.dykes.models import Reading
from .repository_interface import ReadingRepository

class DatabaseReadingRepository(ReadingRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_readings(self) -> List[Reading]:
        result = await self.db.execute(
            select(Reading)
            .options(
                selectinload(Reading.crossection),
                selectinload(Reading.location),
                selectinload(Reading.sensor)
            )
        )
        return result.scalars().all()
