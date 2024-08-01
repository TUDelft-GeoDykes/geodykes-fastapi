'''
Dependency injection: Updated to switch between different data 
source implementations. 
'''
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_db
from app.repositories.database_repository import DatabaseReadingRepository
from app.repositories.inmemory_repository import InMemoryReadingRepository
from app.repositories.repository_interface import ReadingRepository

def get_reading_repository(db: AsyncSession = Depends(get_db)) -> ReadingRepository:
    # You can switch the repository here as needed
    return DatabaseReadingRepository(db)
    # return InMemoryReadingRepository(your_in_memory_data)
