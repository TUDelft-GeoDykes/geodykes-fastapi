# CardCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**front** | **str** |  | 
**back** | **str** |  | [optional] 
**hint** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.card_create import CardCreate

# TODO update the JSON string below
json = "{}"
# create an instance of CardCreate from a JSON string
card_create_instance = CardCreate.from_json(json)
# print the JSON string representation of the object
print(CardCreate.to_json())

# convert the object into a dict
card_create_dict = card_create_instance.to_dict()
# create an instance of CardCreate from a dict
card_create_from_dict = CardCreate.from_dict(card_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


