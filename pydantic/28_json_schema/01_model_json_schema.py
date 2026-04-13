"""
model_json_schema()
===================
Every BaseModel emits a JSON Schema dict -- the same format OpenAPI uses.

Top-level keys you'll see:
  title        -> model class name
  type         -> "object"
  properties   -> {field: {type, title, default, ...}}
  required     -> [fields with no default]
  $defs        -> nested models get hoisted here and $ref'd

Field type -> schema type mapping:
  int    -> "integer"        bool    -> "boolean"
  str    -> "string"         float   -> "number"
  list   -> "array"          dict    -> "object"
  Optional[X]   -> anyOf: [X, null]
  Literal["a"]  -> enum: ["a"]

Uses:
- Feed to datamodel-code-generator -> TS/Go/Python clients.
- Publish as contract between services.
- Embed in OpenAPI without hand-writing YAML.
"""

import json
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    is_active: bool = True  # has default -> not in "required"


schema = User.model_json_schema()
print(json.dumps(schema, indent=2))
# {
#   "title": "User", "type": "object",
#   "properties": {
#     "id":        {"title": "Id",        "type": "integer"},
#     "name":      {"title": "Name",      "type": "string"},
#     "is_active": {"title": "Is Active", "type": "boolean", "default": true}
#   },
#   "required": ["id", "name"]
# }
