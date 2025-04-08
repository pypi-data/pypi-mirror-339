<h1 align="center">Zaptools</h1>

<p align="center">
  <img src="https://raw.githubusercontent.com/NathanDraco22/zaptools-dart/main/assets/zaptools-logo-150.png" />
  <h3 align="center">
    A toolkit for Event-Driven websocket management
  <h3>
</p>
<div align="center">
    <a href="https://pypi.org/project/zaptools/"><img src="https://badge.fury.io/py/zaptools.svg" alt="PyPI version" height="18"></a>
</div>

### Also Supported
| Lang               |Side  |View Source                                                                                           |
|:------------------:|:----:|:------------------------------------------------------------------------------------------------------|
|<a href="https://www.python.org" target="_blank"> <img src="https://www.vectorlogo.zone/logos/dartlang/dartlang-icon.svg" alt="python" width="25" height="25"/> </a>| Client/Server |[`zaptools_dart`](https://github.com/NathanDraco22/zaptools-dart)|

### Getting Started

Zaptools provides tools for building event-driven websocket integration. It includes pre-existing classes to seamless integration with FastApi and Sanic.


#### installation
``` bash
pip install zaptools # windows
pip3 install zaptools # mac
```

#### FastAPI
```python
from fastapi import FastAPI, WebSocket
from zaptools.tools import EventRegister, EventContext
from zaptools.connectors import FastApiConnector

app:FastAPI = FastAPI()
register: EventRegister = EventRegister() 

@register.on_event("hello") 
async def hello_trigger(ctx: EventContext):
    conn = ctx.connection
    await conn.send("hello", "HELLO FROM SERVER !!!") 


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    connector = FastApiConnector(reg, ws)
    await connector.start()

```

Firstly create a `FastAPI` and `EventRegister` instance. `EventRegister` has the responsability to create events.
```python
from fastapi import FastAPI, WebSocket
from zaptools.tools import EventRegister, EventContext, Connector
from zaptools.adapters import FastApiAdapter

app:FastAPI = FastAPI()
register: EventRegister = EventRegister() 
```
For Creating events use the decorator syntax.
This will creates an event named `"hello"` and it will call `hello_trigger` function when an event named `"hello"` is received.
```python
@register.on_event("hello") 
async def hello_trigger(ctx: EventContext):
    conn = ctx.connection
    await conn.send("hello", "HELLO FROM SERVER !!!") 
```
> Event it is a class with name("hello") and the callback(hello_trigger)

For connecting `EventRegister` with the websocket class provided by FastAPI framework, there is a `FastApiConnector`, use the `plug_and_start` static method of the `FastApiConnector`, it will start to receive events.
```python
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    connector = FastApiConnector(reg, ws)
    await connector.start()
```

It's the same way for Sanic Framework
#### Sanic
```python
from sanic import Sanic, Request, Websocket

from zaptools.tools import EventRegister, EventContext
from zaptools.connectors import SanicConnector

app = Sanic("MyHelloWorldApp")
register: EventRegister = EventRegister()

@register.on_event("hello") 
async def hello_trigger(ctx: EventContext):
    conn = ctx.connection
    await conn.send("hello", "HELLO FROM SERVER !!!") 

@app.websocket("/")
async def websocket(request: Request, ws: Websocket):
    connector = SanicConnector(reg, ws)
    await connector.start()

```
### EventContext object
Each element is triggered with a `EventContext` object. This `EventContext` object contains information about the current event and which `WebSocketConnection` is invoking it.
```python
EventContext.event_name # name of current event
EventContext.payload # payload the data from the connection
EventContext.connection # WebSocketConnection 
```
### Sending Events
In order to response to the client use the `WebSocketConnection.send(event:str, payload:Any)`, this object is provided by the `Context`.
```python
@register.on_event("hello") 
async def hello_trigger(ctx: EventContext):
    conn = ctx.connection
    conn.send("hello", "HELLO FROM SERVER !!!") # sending "hello" event to client with a payload.
```
### WebSocketConnection
`WebSocketConnection` provides a easy interaction with the websocket.

```python
WebSocketConnection.id # ID of connection

await WebSocketConnection.send(event:str, payload:Any) #Send Event to the client

await WebSocketConnection.close() # Close the websocket connection
```
> Coroutines need to be awaited.

### Events

The `"connected"`, `"disconnected"` and `"error"` events can be used to trigger an action when a connection is started and after it is closed or when a error ocurred in a event.

```python
@register.on_event("connected")
async def connected_trigger(ctx: EventContext):
    print("Connection started")

@register.on_event("disconnected")
async def disconnected_trigger(ctx: EventContext):
    print("Connection closed")

@register.on_event("error")
async def disconnected_trigger(ctx: EventContext):
    print("An error ocurred in a event")
    print(ctx.payload) # display error details
```
> Error details in `payload`

## Client

Zaptools provides a python client to connect with others zaptools server

```python
from zaptools.client import ZapClient

client = ZapClient()
await client.connect("ws://localhost:8000/") #Connect to the server

await client.send("event1", {"hello":"from client"}, {}) # send a event

# A generator with all event stream
# Receive all events
async for event in client.event_stream(): 
        print(event.payload)


# A generator with all connection state
# Receive connection state
# ONLINE, OFFLINE, CONNNECTING and ERROR state
async for state in client.connection_state(): 
        print(state)

```


## Contributions are wellcome
