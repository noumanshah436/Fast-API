"""
model_dump basics
=================
Model → dict / JSON. The shape you send over HTTP or write to disk.

Method                     Returns     Typical use
----------------------------------------------------------
m.model_dump()             dict        logging, merging, passing around
m.model_dump_json()        str         HTTP response body
m.model_dump_json(indent=2) str        human-readable logs
m.model_dump(mode="json")  dict        dict but with JSON-safe values
                                       (datetime→str, UUID→str, etc.)

Nested models recurse automatically -- no manual walking.
"""

from pydantic import BaseModel


class Address(BaseModel):
    city: str
    country: str


class User(BaseModel):
    id: int
    name: str
    address: Address


u = User(id=1, name="Ada", address=Address(city="London", country="UK"))

print(u.model_dump())         # {'id': 1, 'name': 'Ada', 'address': {...}}
print(u.model_dump_json())    # '{"id":1,"name":"Ada","address":{...}}'
print(u.model_dump_json(indent=2))
