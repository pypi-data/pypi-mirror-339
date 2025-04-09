## Python SDK for GTN Embed

<img src="https://img.shields.io/badge/Python-3.12+-green"/>

This is a lightweight SDK which wraps the REST APIs of the GTN Embed set as documented in the [API Portal](https://developer.globaltradingnetwork.com/rest-api-reference)

### installing packages

The GTN Embed SDK is now available on PyPi

```bash
    pip install gtn-embed-sdk
```

### API Authentication

The GTN Embed uses the notion of Institutions, which represent customers that build their platform upon the GTN Embed.
The end-users of the institution, are referred to as customers.
An institution is able to manage their customers directly and is also able to initiate actions on the user's behalf.

As describe in the [API Portal](https://developer.globaltradingnetwork.com/rest-api-reference) you are required to authenticate
first to the Institution and then as a customer. And resulting keys expire in a certain period, which require
renewing using authentication APIs. However when using the SDK, key renewing is not required since it is
handled by the SDK in background.

The <code>api_url</code> is the API hub where customers are connected to access the GTN Embed. This URL can change depending on
customer's registered country.

#### Initiating API connection

For a connection to be establish, it is required to have following information

* `API URL`, provided by GTN. Can vary depending on the environment (Sandbox, UAT, Production)
* `App Key`, provided by GTN
* `App Secret`, provided by GTN
* `Institution` Code, provided by GTN
* `Customer Number` of the customer initiating the connection. (Optional: only in the customer mode)
* `Private Key` of the institution, provided by GTN

```python
    import gtnapi

    api_credentials = {
        "api_url": "https://api-mena-uat.globaltradingnetwork.com",
        "app_key": "my-app-key",
        "app_secret": "my-app-secret",
        "institution": "MY-INST-CODE",
        "customer_number": "12345678",
        "private_key": "RTRGDBCNKVGJTURI49857YURIEOLFMKJTU5I4O847YRHFJDKDKVFLKTUEJFHRU"
    }

    status = gtnapi.init(**api_credentials)
```

authentication **status** is in the format

```json
    {
        "http_status": 200, 
        "auth_status": "SUCCESS"
    }
```

Once the _**gtnapi.init()**_ is success (i.e. <code>http_code == 200</code>), it is possible to access any REST endpoint (authorised to the customer) by using the SDK.
Request, response parameter and formats are as per the [API Documentation](https://developer.globaltradingnetwork.com/rest-api-reference)

Since the SDK is just a wrapper to the **REST API**, only following methods are available for API endpoints

* `gtnapi.Requests.get()` - for HTTP GET endpoints
* `gtnapi.Requests.post()` - for HTTP POST endpoints
* `gtnapi.Requests.patch()` - for HTTP UPDATE endpoints
* `gtnapi.Requests.delete()` - for HTTP DELETE endpoints

and for streaming data

* `gtnapi.Streaming.TradeData` - for receiving streaming Trade Data
* `gtnapi.Streaming.MarketData` - for receiving streaming Market Data

> [!IMPORTANT]
> SDK does not provide anything not supported by the REST API. See [API Documentation](https://developer.globaltradingnetwork.com/rest-api-reference)

## Examples

### Handling Customers

#### Creating a customer <img src="https://img.shields.io/badge/REST-blue"/>

Call the `HTTP Post` method to the endpoint `customer/account` to create a customer 

```python
    customer = {
      "referenceNumber": "546446546",
      "firstName": "Kevin",
      "lastName": "Smith",
      "passportNumber": "123456",
      ...
    }
    response = gtnapi.Requests.post('/trade/bo/v1.2.1/customer/account', **customer)
    print(json.dumps(response, indent=4))
```
#### Getting customer details <img src="https://img.shields.io/badge/REST-blue"/>
Call the `HTTP Get` method to the endpoint `customer/account` to get customer details 

```python
    response = gtnapi.Requests.get('/trade/bo/v1.2.1/customer/account', customerNumber="12345678")
    print(json.dumps(response, indent=4))
```

Response is in the format

```python
    {
        "http_status" : 200,  # http status of the api call as per the API documentation
        "response" : {data dict}  # response data of the api as per the API documentation
    }
```

### Initiate the Trade Data streaming connection <img src="https://img.shields.io/badge/HTTP Streaming-blue"/>

Can initiate the session by passing endpoint, event type and call-back method references

```python
    gtnapi.Streaming.TradeData.connect('/trade/sse/v1.2.1', 'ORDER', 
                                       on_message=onMessage,
                                       on_close=onClose, 
                                       on_error=onError)
```

Above connection will respond with Order related events when available.
The sdk will call onMessage and other relevant methods when required with relevant data

### Close the streaming connection

can close the Trade Streaming session by calling

```python
    gtnapi.Streaming.TradeData.disconnect()
```

### Market Data APIs

#### Getting snapshot data <img src="https://img.shields.io/badge/REST-blue"/>

```python
    search_params = {
        "source-id": 'NSDQ',
        "keys": "NSDQ~AAPL"
    }
    response = gtnapi.Requests.get('/market-data/realtime/keys/data', **search_params)
    print(json.dumps(response, indent=4))
```

#### Initiate the Market Data streaming connection <img src="https://img.shields.io/badge/Websocket-blue"/>

Can initiate the WS session by passing call-back method references

```python
    gtnapi.Streaming.MarketData.connect("/market-data/websocket/price", 
                                        on_message=onMessage, on_open=onOpen, 
                                        on_close=onClose, on_error=onError)
```

The sdk will call onMessage and other relevant methods when required with relevant data

#### Close the websocket connection

can close the WS session by calling

```python
    gtnapi.Streaming.MarketData.disconnect()
```

### Terminate the API session

The while GTN Embed session will be terminated by calling the following.

```python
    gtnapi.stop()
```

Will terminate
* Access token refresh process
* Active Market Data streaming session
* Active Trade Data streaming session

> [!IMPORTANT]
> Once the session is terminated, any attempt to access endpoints will result in an unauthorised response 

