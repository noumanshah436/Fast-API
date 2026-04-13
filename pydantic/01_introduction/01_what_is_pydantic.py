"""
What is Pydantic?
=================
Runtime data validation using Python type hints.
"""

from pydantic import BaseModel, ValidationError


# Declare a model: fields + types, same syntax as a dataclass.
class User(BaseModel):
    id: int
    name: str
    is_active: bool = True   # default value


# Valid input -- types are coerced where sensible ("1" -> 1, "true" -> True).
u = User(id="1", name="Alice")
print(u)                 # id=1 name='Alice' is_active=True
print(u.model_dump())    # dict form, useful for JSON APIs


# Invalid input -- Pydantic raises a structured error you can surface to clients.
try:
    User(id="not-a-number", name="Bob")
except ValidationError as e:
    # .errors() returns a list of dicts: {loc, msg, type, input}
    print(e.errors()[0])
