
from app.apps.dykes.models import Reading
from .repository_interface import ReadingRepository


class InMemoryReadingRepository(ReadingRepository):
    def __init__(self, data: list[Reading]):
        self.data = data

    async def get_readings(self) -> list[Reading]:
        return self.data
