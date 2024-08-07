#!/usr/bin/env python
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

async def create_locations_and_sensors(session: AsyncSession, sensor_types):
    locations = []
    sensors = []

    # Fetch all topology IDs
    result = await session.execute(sa.select(Topology.id))
    topology_ids = [row[0] for row in result.fetchall()]

    for i in range(1, 6):
        if not topology_ids:
            raise ValueError("No topologies available in the database.")

        topology_id = random.choice(topology_ids)  # Ensure topology_id is valid
        location = LocationInTopology(coordinates=[random.uniform(0, 40), random.uniform(0, 40)], topology_id=topology_id)
        session.add(location)
        await session.flush()  # Ensure location ID is generated
        locations.append(location)  # Append to locations list

        sensors.append(Sensor(name=f"Sensor {i}", sensor_type_id=random.choice(sensor_types).id, location_in_topology_id=location.id, is_active=True))
    
    session.add_all(sensors)  # Add all sensors
    await session.commit()  # Commit both locations and sensors

    return locations, sensors

async def create_readings(session: AsyncSession, crossections, locations, units, sensor_types, sensors):
    readings = []
    start_time = datetime.now() - timedelta(days=30)
    for _ in range(300):
        sensor = random.choice(sensors)
        readings.append(Reading(
            crossection_id=random.choice(crossections).id,
            location_in_topology_id=random.choice(locations).id,
            unit_id=random.choice(units).id,
            sensor_type_id=sensor.sensor_type_id,
            value=random.uniform(10, 100),
            time=start_time + timedelta(hours=random.randint(0, 720)),
            sensor=sensor
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
        locations, sensors = await create_locations_and_sensors(session, sensor_types)
        readings = await create_readings(session, crossections, locations, units, sensor_types, sensors)

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

async def drop_all_tables():
    engine = create_async_engine(DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(drop_tables_sync)

    await engine.dispose()

def drop_tables_sync(connection):
    """To properly handle the inspection of tables using run_sync with
    SQLAlchemy's AsyncConnection, you need to pass a synchronous callable 
    that performs the inspection and table dropping. Here’s how you can adjust 
    the drop_all_tables function:
    """
    # Reflect the existing database into a new metadata object
    metadata = sa.MetaData()
    metadata.reflect(bind=connection)

    # Drop all tables
    for table in reversed(metadata.sorted_tables):
        connection.execute(sa.text(f"DROP TABLE IF EXISTS {table.name} CASCADE"))

    # Drop all other database objects
    connection.execute(sa.text("DROP SCHEMA public CASCADE"))
    connection.execute(sa.text("CREATE SCHEMA public"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Populate development database with synthetic data.')
    parser.add_argument('--reset', action='store_true', help='Reset the database before populating')
    parser.add_argument('--drop-all', action='store_true', help='Drop all tables before populating')
    args = parser.parse_args()

    if args.reset:
        asyncio.run(reset_database())
    elif args.drop_all:
        asyncio.run(drop_all_tables())
    else:
        asyncio.run(create_data())
