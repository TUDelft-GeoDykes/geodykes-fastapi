# DykeSchema

Abstract base class for dyke models, defining essential attributes and providing a foundation for more specific dyke models. It utilizes Python's inheritance mechanism to allow other models to extend this base class without duplicating common attributes.  Attributes:     name (str): Human-readable name of the dyke.     description (Optional[str]): Detailed information about the dyke, if available.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the dyke | 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.dyke_schema import DykeSchema

# TODO update the JSON string below
json = "{}"
# create an instance of DykeSchema from a JSON string
dyke_schema_instance = DykeSchema.from_json(json)
# print the JSON string representation of the object
print(DykeSchema.to_json())

# convert the object into a dict
dyke_schema_dict = dyke_schema_instance.to_dict()
# create an instance of DykeSchema from a dict
dyke_schema_from_dict = DykeSchema.from_dict(dyke_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


