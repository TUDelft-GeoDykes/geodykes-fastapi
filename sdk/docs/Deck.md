# Deck


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**id** | **int** |  | 
**cards** | [**List[Card]**](Card.md) |  | 

## Example

```python
from openapi_client.models.deck import Deck

# TODO update the JSON string below
json = "{}"
# create an instance of Deck from a JSON string
deck_instance = Deck.from_json(json)
# print the JSON string representation of the object
print(Deck.to_json())

# convert the object into a dict
deck_dict = deck_instance.to_dict()
# create an instance of Deck from a dict
deck_from_dict = Deck.from_dict(deck_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


