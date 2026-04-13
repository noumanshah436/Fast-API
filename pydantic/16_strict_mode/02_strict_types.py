"""
Strict types and strict mode
============================
Opt out of coercion per-field or per-model.
"""

from pydantic import BaseModel, ConfigDict, StrictBool, StrictInt, ValidationError


# --- Per-field strictness --------------------------------------------------
class Transfer(BaseModel):
    # Money must never be coerced from a string -- force real ints.
    amount_cents: StrictInt
    confirmed: StrictBool
    # `note` is still lax -- only the sensitive fields are locked down.
    note: str = ""


Transfer(amount_cents=1000, confirmed=True, note="ok")   # fine

try:
    Transfer(amount_cents="1000", confirmed="true")
except ValidationError as e:
    print("rejected:", [err["loc"] for err in e.errors()])
    # [('amount_cents',), ('confirmed',)]


# --- Model-wide strictness -------------------------------------------------
class AuthRequest(BaseModel):
    # Every field is strict; no accidental "false" -> True.
    model_config = ConfigDict(strict=True)

    user_id: int
    token: str
    remember_me: bool


AuthRequest(user_id=7, token="abc", remember_me=False)   # fine

try:
    AuthRequest(user_id="7", token="abc", remember_me="false")
except ValidationError as e:
    print("auth rejected:", len(e.errors()), "errors")


# Rule of thumb:
#   Public HTTP/form endpoints -> default (lax) mode.
#   Money, auth, service-to-service JSON -> strict types / strict config.
