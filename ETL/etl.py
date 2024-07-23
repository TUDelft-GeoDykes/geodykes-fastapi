import csv
from app.apps.dykes.models import Dyke, Crossection, Reading, Sensor, SensorType, UnitOfMeasure, LocationInTopology, Topology

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# import settings from fastAPI module
from app.settings import Settings

from dotenv import load_dotenv
import argparse

load_dotenv()

settings = Settings()

DATABASE_URL = settings.db_dsn  # Adjust your database URL accordingly

# create a session
engine = sa.create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# FILTERS TO PREPROCESS DATASET AND RENAME SENSORS
def get_sensor_name(current_sensor_name):
    # Get the 
    pass

def filter_sensor_type(sensors: list, sensor_type: str) -> list:
    # Filter sensors by type
    pass

# In order to get a sensor name you need process a batch of sensors
def get_sensors_of_dyke(dykename:list) -> list:
    # returns all sensors belonging to a specific dyke
    pass

def get_sensors_in_measurement_vertical(measurement_vertical: list) -> list:
    # We filter those sensors with the same measurement vertical
    pass

def gen_sensor_code(sensor_batch: list) -> str:  
    '''
    >>> gen_sensor_code(get_sensors_in_measurement_vertical(sensor_list))
    '''
    # The list of sensors in a measurement vertical
    pass

# STRATEGY FUNCTIONS TO APPLY TO DIFFERENT CSV FILES
# Dyke strategy func
def load_dyke(row, session):
    pass

# Crossection strategy function
def load_crossection():
    pass

# Unit strategy function

# Sensor type strategy function

# Strategy function to create sensor and its location

# Strategy function to load reading ...

# Strategy for loading data with structure 1
def load_sensor(row, session):
    '''
    A note on the row:
    The row should have the proper name of the
    
    '''
    # Get sensor type id based on name provided in 
    location = "" # gets the location from the name

    sensor = Sensor(name=row["Sensor ID"],
                    sensor_type_id=row["Type"], # How do we get the id by name (Maybe create a method in model)
                    location_in_tpology_id="",
                    is_active=True) # True by default
    
    session.add(sensor)
    session.commit()

# Strategy for loading data with structure 2
def load_structure2(row):
    return {
        "id": row["Identifier"],
        "value": row["Measurement"],
        "timestamp": row["Time"],
        "unit": row["MeasurementUnit"]
    }

# General loader function that takes a strategy function
def load_data(file_path, strategy_func):
    """ A routine to apply a strategy function to a csv file
    """
    loaded_data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data = strategy_func(row)
            loaded_data.append(data)
            # Process each loaded data
            print(f"Processing data: {data}")
            # Add your specific processing logic here
    return loaded_data

# Example usage
if __name__ == "__main__":
    # Create a command line interface where we pass the file path and the strategy function
    parser = argparse.ArgumentParser(description='ETL Command Line Interface')
    parser.add_argument('file_path', type=str, help='Path to the CSV file')
    parser.add_argument('strategy', type=str, choices=['dyke', 'sensor', 'structure2'], help='Strategy function to apply')
    args = parser.parse_args()

    if args.strategy == 'dyke':
        load_data(args.file_path, load_dyke)
    elif args.strategy == 'sensor':
        load_data(args.file_path, load_sensor)
    elif args.strategy == 'structure2':
        load_data(args.file_path, load_structure2)
    else:
         print("Invalid strategy. Please choose 'dyke', 'sensor', or 'structure2'.")