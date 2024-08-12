# openapi_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_cards_api_decks_deck_id_cards_post**](DefaultApi.md#create_cards_api_decks_deck_id_cards_post) | **POST** /api/decks/{deck_id}/cards/ | Create Cards
[**create_deck_api_decks_post**](DefaultApi.md#create_deck_api_decks_post) | **POST** /api/decks/ | Create Deck
[**create_reading_api_readings_post**](DefaultApi.md#create_reading_api_readings_post) | **POST** /api/readings/ | Create Reading
[**create_readings_api_readings_batch2_post**](DefaultApi.md#create_readings_api_readings_batch2_post) | **POST** /api/readings_batch2/ | Create Readings
[**create_readings_in_batch_api_readings_batch_post**](DefaultApi.md#create_readings_in_batch_api_readings_batch_post) | **POST** /api/readings_batch/ | Create Readings In Batch
[**get_card_api_cards_card_id_get**](DefaultApi.md#get_card_api_cards_card_id_get) | **GET** /api/cards/{card_id}/ | Get Card
[**get_deck_api_decks_deck_id_get**](DefaultApi.md#get_deck_api_decks_deck_id_get) | **GET** /api/decks/{deck_id}/ | Get Deck
[**get_dyke_api_dykes_dyke_id_get**](DefaultApi.md#get_dyke_api_dykes_dyke_id_get) | **GET** /api/dykes/{dyke_id}/ | Get Dyke
[**list_cards_api_decks_deck_id_cards_get**](DefaultApi.md#list_cards_api_decks_deck_id_cards_get) | **GET** /api/decks/{deck_id}/cards/ | List Cards
[**list_decks_api_decks_get**](DefaultApi.md#list_decks_api_decks_get) | **GET** /api/decks/ | List Decks
[**list_dykes_api_dykes_get**](DefaultApi.md#list_dykes_api_dykes_get) | **GET** /api/dykes/ | List Dykes
[**list_readings_api_readings_get**](DefaultApi.md#list_readings_api_readings_get) | **GET** /api/readings/ | List Readings
[**update_cards_api_decks_deck_id_cards_put**](DefaultApi.md#update_cards_api_decks_deck_id_cards_put) | **PUT** /api/decks/{deck_id}/cards/ | Update Cards
[**update_deck_api_decks_deck_id_put**](DefaultApi.md#update_deck_api_decks_deck_id_put) | **PUT** /api/decks/{deck_id}/ | Update Deck


# **create_cards_api_decks_deck_id_cards_post**
> Cards create_cards_api_decks_deck_id_cards_post(deck_id, card_create)

Create Cards

### Example


```python
import openapi_client
from openapi_client.models.card_create import CardCreate
from openapi_client.models.cards import Cards
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    deck_id = 56 # int | 
    card_create = [openapi_client.CardCreate()] # List[CardCreate] | 

    try:
        # Create Cards
        api_response = api_instance.create_cards_api_decks_deck_id_cards_post(deck_id, card_create)
        print("The response of DefaultApi->create_cards_api_decks_deck_id_cards_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_cards_api_decks_deck_id_cards_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **deck_id** | **int**|  | 
 **card_create** | [**List[CardCreate]**](CardCreate.md)|  | 

### Return type

[**Cards**](Cards.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_deck_api_decks_post**
> Deck create_deck_api_decks_post(deck_create)

Create Deck

### Example


```python
import openapi_client
from openapi_client.models.deck import Deck
from openapi_client.models.deck_create import DeckCreate
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    deck_create = openapi_client.DeckCreate() # DeckCreate | 

    try:
        # Create Deck
        api_response = api_instance.create_deck_api_decks_post(deck_create)
        print("The response of DefaultApi->create_deck_api_decks_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_deck_api_decks_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **deck_create** | [**DeckCreate**](DeckCreate.md)|  | 

### Return type

[**Deck**](Deck.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_reading_api_readings_post**
> object create_reading_api_readings_post(reading)

Create Reading

payload_example = { \"crossection\": \"Crossection 2-2\",   \"location_in_topology\": [     36.20784624264615,     13.973984822788621   ],   \"unit\": \"Unit 5\",   \"value\": 40,   \"time\": \"2024-09-30T23:20:35.286428\" }

### Example


```python
import openapi_client
from openapi_client.models.reading import Reading
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    reading = openapi_client.Reading() # Reading | 

    try:
        # Create Reading
        api_response = api_instance.create_reading_api_readings_post(reading)
        print("The response of DefaultApi->create_reading_api_readings_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_reading_api_readings_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **reading** | [**Reading**](Reading.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_readings_api_readings_batch2_post**
> object create_readings_api_readings_batch2_post(reading)

Create Readings

This is the description of the concept of this endpoint

### Example


```python
import openapi_client
from openapi_client.models.reading import Reading
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    reading = [openapi_client.Reading()] # List[Reading] | 

    try:
        # Create Readings
        api_response = api_instance.create_readings_api_readings_batch2_post(reading)
        print("The response of DefaultApi->create_readings_api_readings_batch2_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_readings_api_readings_batch2_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **reading** | [**List[Reading]**](Reading.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_readings_in_batch_api_readings_batch_post**
> object create_readings_in_batch_api_readings_batch_post()

Create Readings In Batch

A prototype for this endpoint testing the main concept. USE CASE: A user provides a csv file with readings, or python loaded dictionaries with readings (I am assuming csv is more appropriate for this case) The user also needs to provide a header to the endpoint that identifies: - The metadata should have the following fields: - The sensor this data is coming from - The sensor should be related to an id in the database - Alternatively the user can create a new sensor first. - If the following fields are not provided, the endpoint should return an error.   USE CASE B: - The user has a csv file and list where there are different sensors - The name of the sensor is used to identify the sensor and perform the check - How it should work: The file is uploaded, the endpoint reads the file and checks the sensor name    - Use yield to iterate over the file and check the sensor name

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)

    try:
        # Create Readings In Batch
        api_response = api_instance.create_readings_in_batch_api_readings_batch_post()
        print("The response of DefaultApi->create_readings_in_batch_api_readings_batch_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_readings_in_batch_api_readings_batch_post: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_card_api_cards_card_id_get**
> Card get_card_api_cards_card_id_get(card_id)

Get Card

### Example


```python
import openapi_client
from openapi_client.models.card import Card
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    card_id = 56 # int | 

    try:
        # Get Card
        api_response = api_instance.get_card_api_cards_card_id_get(card_id)
        print("The response of DefaultApi->get_card_api_cards_card_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_card_api_cards_card_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **card_id** | **int**|  | 

### Return type

[**Card**](Card.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_deck_api_decks_deck_id_get**
> Deck get_deck_api_decks_deck_id_get(deck_id)

Get Deck

### Example


```python
import openapi_client
from openapi_client.models.deck import Deck
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    deck_id = 56 # int | 

    try:
        # Get Deck
        api_response = api_instance.get_deck_api_decks_deck_id_get(deck_id)
        print("The response of DefaultApi->get_deck_api_decks_deck_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_deck_api_decks_deck_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **deck_id** | **int**|  | 

### Return type

[**Deck**](Deck.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dyke_api_dykes_dyke_id_get**
> DykeSchema get_dyke_api_dykes_dyke_id_get(dyke_id)

Get Dyke

### Example


```python
import openapi_client
from openapi_client.models.dyke_schema import DykeSchema
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    dyke_id = 56 # int | 

    try:
        # Get Dyke
        api_response = api_instance.get_dyke_api_dykes_dyke_id_get(dyke_id)
        print("The response of DefaultApi->get_dyke_api_dykes_dyke_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_dyke_api_dykes_dyke_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dyke_id** | **int**|  | 

### Return type

[**DykeSchema**](DykeSchema.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_cards_api_decks_deck_id_cards_get**
> Cards list_cards_api_decks_deck_id_cards_get(deck_id)

List Cards

### Example


```python
import openapi_client
from openapi_client.models.cards import Cards
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    deck_id = 56 # int | 

    try:
        # List Cards
        api_response = api_instance.list_cards_api_decks_deck_id_cards_get(deck_id)
        print("The response of DefaultApi->list_cards_api_decks_deck_id_cards_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_cards_api_decks_deck_id_cards_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **deck_id** | **int**|  | 

### Return type

[**Cards**](Cards.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_decks_api_decks_get**
> Decks list_decks_api_decks_get()

List Decks

### Example


```python
import openapi_client
from openapi_client.models.decks import Decks
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)

    try:
        # List Decks
        api_response = api_instance.list_decks_api_decks_get()
        print("The response of DefaultApi->list_decks_api_decks_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_decks_api_decks_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Decks**](Decks.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_dykes_api_dykes_get**
> Dykes list_dykes_api_dykes_get()

List Dykes

### Example


```python
import openapi_client
from openapi_client.models.dykes import Dykes
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)

    try:
        # List Dykes
        api_response = api_instance.list_dykes_api_dykes_get()
        print("The response of DefaultApi->list_dykes_api_dykes_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_dykes_api_dykes_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Dykes**](Dykes.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_readings_api_readings_get**
> Readings list_readings_api_readings_get(start_date=start_date, end_date=end_date, sensor_id=sensor_id, sensor_name=sensor_name)

List Readings

Retrieve readings from the database asynchronously. The user should be able to filter readings by start date, end date, and sensor ID. These parameters are optional and should allow to flexible query different subsets of readings.  Args:     start_date (Optional[datetime]): The start date to filter readings by.     end_date (Optional[datetime]): The end date to filter readings by.     sensor_id (Optional[int]): The sensor ID to filter readings by.     sensor_name (Optional[str]): The sensor name to filter readings by.

### Example


```python
import openapi_client
from openapi_client.models.readings import Readings
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    start_date = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    end_date = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    sensor_id = [56] # List[int] |  (optional)
    sensor_name = ['sensor_name_example'] # List[str] |  (optional)

    try:
        # List Readings
        api_response = api_instance.list_readings_api_readings_get(start_date=start_date, end_date=end_date, sensor_id=sensor_id, sensor_name=sensor_name)
        print("The response of DefaultApi->list_readings_api_readings_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_readings_api_readings_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **datetime**|  | [optional] 
 **end_date** | **datetime**|  | [optional] 
 **sensor_id** | [**List[int]**](int.md)|  | [optional] 
 **sensor_name** | [**List[str]**](str.md)|  | [optional] 

### Return type

[**Readings**](Readings.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_cards_api_decks_deck_id_cards_put**
> Cards update_cards_api_decks_deck_id_cards_put(deck_id, card)

Update Cards

### Example


```python
import openapi_client
from openapi_client.models.card import Card
from openapi_client.models.cards import Cards
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    deck_id = 56 # int | 
    card = [openapi_client.Card()] # List[Card] | 

    try:
        # Update Cards
        api_response = api_instance.update_cards_api_decks_deck_id_cards_put(deck_id, card)
        print("The response of DefaultApi->update_cards_api_decks_deck_id_cards_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->update_cards_api_decks_deck_id_cards_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **deck_id** | **int**|  | 
 **card** | [**List[Card]**](Card.md)|  | 

### Return type

[**Cards**](Cards.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_deck_api_decks_deck_id_put**
> Deck update_deck_api_decks_deck_id_put(deck_id, deck_create)

Update Deck

### Example


```python
import openapi_client
from openapi_client.models.deck import Deck
from openapi_client.models.deck_create import DeckCreate
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    deck_id = 56 # int | 
    deck_create = openapi_client.DeckCreate() # DeckCreate | 

    try:
        # Update Deck
        api_response = api_instance.update_deck_api_decks_deck_id_put(deck_id, deck_create)
        print("The response of DefaultApi->update_deck_api_decks_deck_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->update_deck_api_decks_deck_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **deck_id** | **int**|  | 
 **deck_create** | [**DeckCreate**](DeckCreate.md)|  | 

### Return type

[**Deck**](Deck.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

