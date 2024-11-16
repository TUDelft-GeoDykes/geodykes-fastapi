import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.repositories.database_repository import DatabaseReadingRepository
from app.settings import settings


# Assuming you have the following configurations
DATABASE_URL = settings.db_dsn

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session factory
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession,
)

# Create an instance of the repository
async def create_repository(session):
    return DatabaseReadingRepository(db=session)

# Create an instance of the repository
# repo = asyncio.run(create_repository())

# Function to get all readings
async def get_readings():
    async with async_session() as session:
        repo = await create_repository(session)
        return await repo.get_readings()

# Run the function and get the result
items = asyncio.run(get_readings())
