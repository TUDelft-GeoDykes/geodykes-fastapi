# Readings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**readings** | [**List[Reading]**](Reading.md) |  | 

## Example

```python
from openapi_client.models.readings import Readings

# TODO update the JSON string below
json = "{}"
# create an instance of Readings from a JSON string
readings_instance = Readings.from_json(json)
# print the JSON string representation of the object
print(Readings.to_json())

# convert the object into a dict
readings_dict = readings_instance.to_dict()
# create an instance of Readings from a dict
readings_from_dict = Readings.from_dict(readings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


