"""
model_json_schema()
===================
Ask any model for its JSON Schema -- the same format used by OpenAPI.
"""

import json
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    is_active: bool = True


schema = User.model_json_schema()
print(json.dumps(schema, indent=2))


# Typical output contains:
# - "title": model name
# - "type": "object"
# - "properties": {field_name: {type, ...}}
# - "required": [names of fields with no default]
#
# Example (abridged):
# {
#   "title": "User",
#   "type": "object",
#   "properties": {
#     "id":        {"title": "Id",        "type": "integer"},
#     "name":      {"title": "Name",      "type": "string"},
#     "is_active": {"title": "Is Active", "type": "boolean", "default": true}
#   },
#   "required": ["id", "name"]
# }


# Why this is useful:
# - Feed it to tools like datamodel-code-generator to build clients.
# - Publish it so consumers can validate requests before sending.
# - Embed it in OpenAPI docs without writing YAML by hand.
