"""
Parsing a list of models
========================
Top-level JSON arrays via TypeAdapter.
"""

import json

from pydantic import BaseModel, TypeAdapter


class User(BaseModel):
    id: int
    name: str
    is_active: bool = True


# Imagine a GET /users endpoint returning a JSON array (not an object).
raw = json.dumps([
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob", "is_active": False},
    {"id": "3", "name": "Carol"},   # coerced to int
])

# BaseModel.model_validate_json expects an object, not an array.
# TypeAdapter is the v2 way to validate arbitrary type expressions.
users_adapter = TypeAdapter(list[User])
users = users_adapter.validate_json(raw)

for u in users:
    print(u)

# Serialize the whole list back to JSON in one call.
print(users_adapter.dump_json(users).decode())


# TypeAdapter also handles dict[str, User], tuple[User, ...], Union[...], etc.
# -- use it whenever the top-level type is not a single BaseModel.
