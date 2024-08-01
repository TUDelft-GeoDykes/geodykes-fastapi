from typing import List
from app.apps.dykes.models import Reading
from .repository_interface import ReadingRepository

class InMemoryReadingRepository(ReadingRepository):
    def __init__(self, data: List[Reading]):
        self.data = data

    async def get_all_readings(self) -> List[Reading]:
        return self.data
