"""
Handling Invalid Input
======================
Malformed JSON, bad types, and opting out of lax coercion with strict=True.

Failure modes and the `type` you'll see
---------------------------------------
malformed JSON                 →  json_invalid
missing required field         →  missing
wrong type (lax can't coerce)  →  int_parsing · bool_parsing · ...
strict=True rejects coercion   →  int_type · bool_type · ...

Lax vs strict — quick rule
--------------------------
lax (default)   →  accept "1"/"true"/"2025-01-01"  — great for HTTP/CLI input
strict=True     →  types must match exactly        — for trusted upstream (Protobuf, internal RPC)

Scoping strict
--------------
- Per call:  Model.model_validate(data, strict=True)
- Per model: model_config = ConfigDict(strict=True)
"""

from pydantic import BaseModel, ValidationError


class LoginRequest(BaseModel):
    username: str
    remember_me: bool


# 1. Malformed JSON — surfaces as a ValidationError, not a JSONDecodeError.
try:
    LoginRequest.model_validate_json('{"username": "alice", "remember_me": tru')
except ValidationError as e:
    print("bad json:", e.errors()[0]["type"])   # json_invalid


# 2. Lax (default): "true"/"false"/1/0 are coerced; "yes"/"no" are NOT.
lax = LoginRequest.model_validate({"username": "alice", "remember_me": "true"})
print("lax:", lax.remember_me)   # True


# 3. strict=True — reject coercion. Use when the producer guarantees exact types
# and you want drift (e.g., string "true" leaking in) to fail loudly.
try:
    LoginRequest.model_validate(
        {"username": "alice", "remember_me": "true"},
        strict=True,
    )
except ValidationError as e:
    print("strict:", e.errors()[0]["type"])   # bool_type


# 4. strict=True still succeeds when types already match exactly.
ok = LoginRequest.model_validate({"username": "alice", "remember_me": True}, strict=True)
print("strict ok:", ok)
