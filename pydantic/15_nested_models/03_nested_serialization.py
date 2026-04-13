"""
Nested serialization
====================
model_dump recurses into nested models and lists automatically.
"""

from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    country: str


class Company(BaseModel):
    name: str
    address: Address


class Employee(BaseModel):
    id: int
    name: str
    company: Company
    skills: list[str]


emp = Employee(
    id=1,
    name="Alice",
    company=Company(
        name="Acme",
        address=Address(street="1 Main", city="Berlin", country="DE"),
    ),
    skills=["python", "pydantic"],
)

# Python dict -- nested models become nested dicts, all the way down.
print(emp.model_dump())
# {'id': 1, 'name': 'Alice',
#  'company': {'name': 'Acme',
#              'address': {'street': '1 Main', 'city': 'Berlin',
#                          'country': 'DE'}},
#  'skills': ['python', 'pydantic']}

# JSON string -- ready to return from FastAPI.
print(emp.model_dump_json(indent=2))

# Common tweaks:
#   exclude={"company": {"address"}}   -> drop nested field
#   exclude_none=True                  -> omit None values
#   by_alias=True                      -> use field aliases in output
print(emp.model_dump(exclude={"company": {"address"}}))
