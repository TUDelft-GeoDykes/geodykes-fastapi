from services.interface import get_readings
from services.openapi import _get_readings, _get_client

if __name__ == "__main__":
    api_client = _get_client()

    # Fetch readings using different parameters
    readings_by_date = get_readings(_get_readings, 
                                    api_client=api_client, 
                                    start_date="2024-07-26T13:48:14.460881",
                                    end_date="2024-08-03T11:48:14.460881")
    readings_by_sensor = get_readings(_get_readings, 
                                      api_client=api_client, 
                                      sensor_name=["Sensor 1"])
    # Print the first reading from each list
    print("Readings by date:")
    print("Type of readings_by_date: ", type(readings_by_date))
    print(readings_by_date.readings[0])

    # Print the first reading from each list
    print("Readings by sensor:")
    print("Type of readings_by_sensor: ", type(readings_by_sensor))
    print(readings_by_sensor.readings[0])