# Card


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**front** | **str** |  | 
**back** | **str** |  | [optional] 
**hint** | **str** |  | [optional] 
**id** | **int** |  | 
**deck_id** | **int** |  | [optional] 

## Example

```python
from openapi_client.models.card import Card

# TODO update the JSON string below
json = "{}"
# create an instance of Card from a JSON string
card_instance = Card.from_json(json)
# print the JSON string representation of the object
print(Card.to_json())

# convert the object into a dict
card_dict = card_instance.to_dict()
# create an instance of Card from a dict
card_from_dict = Card.from_dict(card_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


