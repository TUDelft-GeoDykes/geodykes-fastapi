from dotenv import load_dotenv
import os

from openapi_client import ApiClient, Configuration
from openapi_client.api.default_api import DefaultApi

load_dotenv()


def _get_client(url="http://localhost:8000") -> DefaultApi:
    """
    Create an instance of the API client.
    
    Returns:
        DefaultApi: An instance of the API client.
    """
    configuration = Configuration(host=url)
    return DefaultApi(ApiClient(configuration))

def _get_readings(api_client, start_date=None, end_date=None, sensor_id=None, sensor_name=None) -> list:
    """
    Fetch readings from the OpenAPI client based on provided parameters.
    
    Args:
        api_client (DefaultApi): An instance of the API client.
        start_date (str, optional): Start date for filtering readings.
        end_date (str, optional): End date for filtering readings.
        sensor_id (int, optional): Sensor ID for filtering readings.

    Returns:
        List[dict]: The API response containing readings.
    """
    try:
        api_response = api_client.list_readings_api_readings_get(
            start_date=start_date, 
            end_date=end_date, 
            sensor_id=sensor_id,
            sensor_name=sensor_name
        )
        return api_response
    except Exception as e:
        print(f"Exception when calling API: {e}")
        return None