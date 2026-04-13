"""
Handling Invalid Input
======================
Malformed JSON, type errors, and opting out of coercion with strict=True.
"""

from pydantic import BaseModel, ValidationError


class LoginRequest(BaseModel):
    username: str
    remember_me: bool


# 1. Malformed JSON -- surfaces as a ValidationError with type="json_invalid".
try:
    LoginRequest.model_validate_json('{"username": "alice", "remember_me": tru')
except ValidationError as e:
    print("bad json:", e.errors()[0]["type"])


# 2. Default (lax) mode -- Pydantic coerces reasonable inputs.
# "yes"/"no" are NOT coerced, but "true"/"false"/1/0 are.
lax = LoginRequest.model_validate({"username": "alice", "remember_me": "true"})
print("lax:", lax.remember_me)   # True


# 3. Strict mode -- disables coercion for that call.
# Use when upstream guarantees exact types (e.g., Protobuf, trusted services)
# and you want to catch accidental string-vs-bool drift early.
try:
    LoginRequest.model_validate(
        {"username": "alice", "remember_me": "true"},
        strict=True,
    )
except ValidationError as e:
    print("strict:", e.errors()[0]["type"])   # bool_type


# 4. Strict mode still succeeds when types already match exactly.
strict_ok = LoginRequest.model_validate(
    {"username": "alice", "remember_me": True},
    strict=True,
)
print("strict ok:", strict_ok)
