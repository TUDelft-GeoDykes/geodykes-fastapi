# DeckCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.deck_create import DeckCreate

# TODO update the JSON string below
json = "{}"
# create an instance of DeckCreate from a JSON string
deck_create_instance = DeckCreate.from_json(json)
# print the JSON string representation of the object
print(DeckCreate.to_json())

# convert the object into a dict
deck_create_dict = deck_create_instance.to_dict()
# create an instance of DeckCreate from a dict
deck_create_from_dict = DeckCreate.from_dict(deck_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


