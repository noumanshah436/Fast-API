"""
model_dump basics
=================
Serialize models to dict / JSON -- the shape you send over HTTP.
"""

from pydantic import BaseModel


class Address(BaseModel):
    city: str
    country: str


class User(BaseModel):
    id: int
    name: str
    address: Address  # nested models dump recursively


u = User(id=1, name="Ada", address=Address(city="London", country="UK"))

# dict form -- handy for merging, logging, or passing to non-JSON sinks.
print(u.model_dump())
# {'id': 1, 'name': 'Ada', 'address': {'city': 'London', 'country': 'UK'}}

# JSON string -- ready to return from an HTTP handler.
print(u.model_dump_json())
# {"id":1,"name":"Ada","address":{"city":"London","country":"UK"}}

# model_dump_json takes indent for human-readable logs.
print(u.model_dump_json(indent=2))
