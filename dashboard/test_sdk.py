from openapi_client import ApiClient, Configuration
from openapi_client.api.default_api import DefaultApi

# Configure API key authorization: ApiKeyAuth
configuration = Configuration()
configuration.host = "http://localhost:8000"

# Create an API client with the configuration
client = ApiClient(configuration)

# Create an instance of the API class
api_instance = DefaultApi(client)

# api_instance.list_readings_api_readings_get

# Example of using the SDK to list readings
try:
    api_response = api_instance.list_readings_api_readings_get(sensor_name=["Sensor 1", "Sensor 2"])
    print(api_response)
except Exception as e:
    print("Exception when calling API: %s\n" % e)

# from openapi_client.models.readings import Readings

# # TODO update the JSON string below
# json = "{}"
# # create an instance of Readings from a JSON string
# readings_instance = Readings.from_json(json)
# # print the JSON string representation of the object
# print(Readings.to_json())

# # convert the object into a dict
# readings_dict = readings_instance.to_dict()
# # create an instance of Readings from a dict
# readings_from_dict = Readings.from_dict(readings_dict)
