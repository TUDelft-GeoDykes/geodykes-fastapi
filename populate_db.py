'''
Python script to populate your development database with synthetic data. 
This script uses SQLAlchemy to interact with the database and will create 4 different dykes, 5 different types of sensors, 5 different units, and 300 readings

'''
import asyncio
from datetime import datetime, timedelta
import random

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.apps.dykes.models import Dyke, Crossection, Reading, Sensor, SensorType, UnitOfMeasure, LocationInTopology, Topology

# import settings from fastAPI module
from app.settings import Settings

from dotenv import load_dotenv
import argparse

load_dotenv()

settings = Settings()

DATABASE_URL = settings.db_dsn  # Adjust your database URL accordingly

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_dykes(session: AsyncSession):
    dykes = [Dyke(name=f"Dyke {i}", description=f"Description for Dyke {i}") for i in range(1, 5)]
    session.add_all(dykes)
    await session.commit()
    return dykes

# create topologies
async def create_topologies(session: AsyncSession):
    '''
    # Create a function to randomly generate a json list of X, Y coordinates
    '''
    def generate_coordinates():
        coordinates = []
        for _ in range(6):
            coordinate = {"x": random.uniform(0, 10), "y": random.uniform(0, 10)}
            coordinates.append(coordinate)
        return coordinates

    topologies = []
    for j in range(1, 40):
        topologies.append(Topology(coordinates=generate_coordinates()))
    session.add_all(topologies)
    await session.commit()
    return topologies

async def create_crossections(session: AsyncSession, dykes):
    # This will be created manually
    crossections = []
    for dyke in dykes:
        for j in range(1, 3):
            crossections.append(Crossection(dyke_id=dyke.id, name=f"Crossection {dyke.id}-{j}", description=f"Description for Crossection {dyke.id}-{j}", topology=f"Topology {dyke.id}-{j}"))
    session.add_all(crossections)
    await session.commit()
    return crossections


async def create_units(session: AsyncSession):
    # This will be created manually
    units = [UnitOfMeasure(unit=f"Unit {i}", description=f"Description for Unit {i}") for i in range(1, 6)]
    session.add_all(units)
    await session.commit()
    return units

async def create_sensor_types(session: AsyncSession):
    # This will be created manually
    sensor_types = [SensorType(name=f"SensorType {i}", details=f"Details for SensorType {i}", multisensor=bool(i % 2)) for i in range(1, 6)]
    session.add_all(sensor_types)
    await session.commit()
    return sensor_types

async def create_locations_and_sensors(session: AsyncSession, crossections, sensor_types):
    # CSV table to be read
    locations = []
    sensors = []
    for i in range(1, 6):
        print("DEBUG")
        print(random.choice(crossections).id)
        location = LocationInTopology(coordinates=[random.uniform(0, 10), random.uniform(0, 10)], topology_id=random.choice(crossections).id)
        locations.append(location)
        sensors.append(Sensor(name=f"Sensor {i}", sensor_type_id=random.choice(sensor_types).id, location_in_topology_id=location.id, is_active=True))
    session.add_all(locations)
    session.add_all(sensors)
    await session.commit()
    return locations, sensors

async def create_readings(session: AsyncSession, crossections, locations, units, sensor_types):
    readings = []
    start_time = datetime.now() - timedelta(days=30)
    for _ in range(300):
        readings.append(Reading(
            crossection_id=random.choice(crossections).id,
            location_in_topology_id=random.choice(locations).id,
            unit_id=random.choice(units).id,
            sensor_type_id=random.choice(sensor_types).id,
            value=random.uniform(10, 100),
            time=start_time + timedelta(hours=random.randint(0, 720))
        ))
    session.add_all(readings)
    await session.commit()
    return readings

async def create_data():
    async with SessionLocal() as session:
        dykes = await create_dykes(session)
        topologies = await create_topologies(session)
        crossections = await create_crossections(session, dykes)
        units = await create_units(session)
        sensor_types = await create_sensor_types(session)
        locations, sensors = await create_locations_and_sensors(session, crossections, sensor_types)
        # readings = await create_readings(session, crossections, locations, units, sensor_types)

async def reset_database():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        # Fetch all table names
        result = await conn.execute(
            sa.text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        )
        tables = result.fetchall()
        
        # Disable foreign key checks
        await conn.execute(sa.text("SET session_replication_role = 'replica';"))

        # Truncate all tables
        for table in tables:
            await conn.execute(sa.text(f"TRUNCATE TABLE {table[0]} CASCADE;"))
        
        # Enable foreign key checks
        await conn.execute(sa.text("SET session_replication_role = 'origin';"))

# async def reset_database():
#     engine = create_async_engine(DATABASE_URL, echo=True)
#     async with engine.begin() as conn:
#         await conn.execute(sa.text("DROP SCHEMA public CASCADE;"))
#         await conn.execute(sa.text("CREATE SCHEMA public;"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Populate development database with synthetic data.')
    parser.add_argument('--reset', action='store_true', help='Reset the database before populating')
    args = parser.parse_args()

    if args.reset:
        asyncio.run(reset_database())
    else:
        asyncio.run(create_data())
