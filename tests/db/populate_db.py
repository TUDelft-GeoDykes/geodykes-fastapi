#!/usr/bin/env python
'''
Python script to populate your development database with synthetic data.
This script uses SQLAlchemy to interact with the database asynchronously and will create 4 different dykes, 5 different types of sensors, 5 different units, and 300 readings.
'''

import asyncio
from datetime import datetime, timedelta
import random

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, selectinload

from app.apps.dykes.models import Dyke, Crossection, Reading, Sensor, SensorType, UnitOfMeasure, LocationInTopology, Topology
from app.settings import Settings
from dotenv import load_dotenv
import argparse

# Load environment variables from a .env file
load_dotenv()

# Load application settings
settings = Settings()

# Database URL retrieved from the settings
DATABASE_URL = settings.db_dsn

# Create an async engine for interacting with the database
# `echo=True` enables logging of all SQL queries for debugging purposes
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory that will generate async sessions for interacting with the database
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def generate_coordinates():
    """Generate a list of random (x, y) coordinate pairs."""
    return [{"x": random.uniform(0, 10), "y": random.uniform(0, 10)} for _ in range(6)]

async def create_dykes(session: AsyncSession):
    """Create multiple Dyke entries in the database."""
    dykes = [Dyke(name=f"Dyke {i}", description=f"Description for Dyke {i}") for i in range(1, 5)]
    session.add_all(dykes)  # Add all dyke objects to the session
    await session.commit()  # Commit the transaction to persist changes in the database
    return dykes

async def create_topologies(session: AsyncSession):
    """Create multiple Topology entries in the database with random coordinates."""
    topologies = [Topology(coordinates=generate_coordinates()) for _ in range(1, 40)]
    session.add_all(topologies)
    await session.commit()
    return topologies

async def create_crossections(session: AsyncSession, dykes):
    """Create Crossection entries for each dyke with associated topology data."""
    crossections = []
    for dyke in dykes:
        for j in range(1, 3):
            topology_data = generate_coordinates()  # Generate random topology data
            crossections.append(Crossection(
                dyke_id=dyke.id, 
                name=f"Crossection {dyke.id}-{j}", 
                description=f"Description for Crossection {dyke.id}-{j}",
                topology=topology_data
            ))
    session.add_all(crossections)
    await session.commit()
    return crossections

async def create_units(session: AsyncSession):
    """Create UnitOfMeasure entries in the database."""
    units = [UnitOfMeasure(unit=f"Unit {i}", description=f"Description for Unit {i}") for i in range(1, 6)]
    session.add_all(units)
    await session.commit()
    return units

async def create_sensor_types(session: AsyncSession):
    """Create SensorType entries in the database."""
    sensor_types = [SensorType(name=f"SensorType {i}", details=f"Details for SensorType {i}", multisensor=bool(i % 2)) for i in range(1, 6)]
    session.add_all(sensor_types)
    await session.commit()
    return sensor_types

async def associate_sensor_types_with_units(session: AsyncSession, sensor_types, units):
    """
    Associate each SensorType with a set of UnitOfMeasure entries.
    
    Eager loading of the `units_of_measure` relationship is performed using selectinload.
    This ensures that the relationship is properly loaded in the async context before we append units.
    """
    sensor_types = await session.execute(
        sa.select(SensorType).options(selectinload(SensorType.units_of_measure))
    )
    sensor_types = sensor_types.scalars().all()

    for sensor_type in sensor_types:
        # Number of units to associate depends on whether it's a multisensor
        num_units = random.randint(2, len(units)) if sensor_type.multisensor else 1
        selected_units = random.sample(units, k=num_units)  # Randomly select units

        # Append each selected unit to the sensor type's units_of_measure relationship
        for unit in selected_units:
            sensor_type.units_of_measure.append(unit)

    await session.commit()  # Commit the transaction to save changes

async def create_locations_and_sensors(session: AsyncSession, sensor_types):
    """
    Create LocationInTopology and Sensor entries in the database.
    
    Each sensor is linked to a specific location and a sensor type.
    """
    locations = []
    sensors = []

    # Fetch all available crossection IDs to associate with locations
    result = await session.execute(sa.select(Crossection.id))
    crossection_ids = [row[0] for row in result.fetchall()]

    if not crossection_ids:
        raise ValueError("No crossections available in the database.")

    for i in range(1, 6):
        crossection_id = random.choice(crossection_ids)  # Select a random crossection ID
        location = LocationInTopology(coordinates=[random.uniform(0, 40), random.uniform(0, 40)], crossection_id=crossection_id)
        session.add(location)
        await session.flush()  # Ensure location ID is generated and available
        locations.append(location)
        sensors.append(Sensor(name=f"Sensor {i}", sensor_type_id=random.choice(sensor_types).id, location_in_topology_id=location.id, is_active=True))

    session.add_all(sensors)  # Add all sensors to the session
    await session.commit()  # Commit the transaction to save changes

    return locations, sensors

async def create_readings(session: AsyncSession, crossections, locations, units, sensor_types, sensors):
    """
    Create Reading entries in the database.

    Each reading is associated with a specific crossection, location, unit, sensor type, and sensor.
    """
    readings = []
    start_time = datetime.now() - timedelta(days=30)  # Start time for generating readings

    for _ in range(300):  # Create 300 readings
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
    await session.commit()  # Commit the transaction to save all readings

    return readings

async def create_data():
    """Main function to create all data entries in the database."""
    async with SessionLocal() as session:  # Create a new session
        dykes = await create_dykes(session)
        await create_topologies(session)
        crossections = await create_crossections(session, dykes)
        units = await create_units(session)
        sensor_types = await create_sensor_types(session)

        # Associate sensor types with units
        await associate_sensor_types_with_units(session, sensor_types, units)

        locations, sensors = await create_locations_and_sensors(session, sensor_types)
        await create_readings(session, crossections, locations, units, sensor_types, sensors)

async def reset_database():
    """Reset the database by truncating all tables."""
    async with engine.begin() as conn:
        result = await conn.execute(sa.text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';"))
        tables = result.fetchall()
        await conn.execute(sa.text("SET session_replication_role = 'replica';"))  # Disable foreign key checks
        for table in tables:
            await conn.execute(sa.text(f"TRUNCATE TABLE {table[0]} CASCADE;"))
        await conn.execute(sa.text("SET session_replication_role = 'origin';"))  # Re-enable foreign key checks

async def drop_all_tables():
    """Drop all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(drop_tables_sync)  # Execute synchronous drop in the async context
    await engine.dispose()

def drop_tables_sync(connection):
    """Helper function to drop all tables in a synchronous context."""
    metadata = sa.MetaData()
    metadata.reflect(bind=connection)
    for table in reversed(metadata.sorted_tables):
        connection.execute(sa.text(f"DROP TABLE IF EXISTS {table.name} CASCADE"))
    connection.execute(sa.text("DROP SCHEMA public CASCADE"))
    connection.execute(sa.text("CREATE SCHEMA public"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Populate development database with synthetic data.')
    parser.add_argument('--reset', action='store_true', help='Reset the database before populating')
    parser.add_argument('--drop-all', action='store_true', help='Drop all tables before populating')
    args = parser.parse_args()

    if args.reset:
        asyncio.run(reset_database())  # Run the reset_database function if --reset flag is used
    elif args.drop_all:
        asyncio.run(drop_all_tables())  # Run the drop_all_tables function if --drop-all flag is used
    else:
        asyncio.run(create_data())  # Run the create_data function to populate the database
