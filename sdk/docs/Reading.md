# Reading


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**crossection** | **str** |  | 
**sensor_id** | **int** |  | 
**sensor_name** | **str** |  | 
**sensor_type** | **str** |  | 
**sensor_location** | **List[float]** |  | 
**sensor_is_active** | **bool** |  | 
**location_in_topology** | **List[float]** |  | 
**unit** | **str** |  | 
**value** | **float** |  | 
**time** | **datetime** |  | 

## Example

```python
from openapi_client.models.reading import Reading

# TODO update the JSON string below
json = "{}"
# create an instance of Reading from a JSON string
reading_instance = Reading.from_json(json)
# print the JSON string representation of the object
print(Reading.to_json())

# convert the object into a dict
reading_dict = reading_instance.to_dict()
# create an instance of Reading from a dict
reading_from_dict = Reading.from_dict(reading_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


