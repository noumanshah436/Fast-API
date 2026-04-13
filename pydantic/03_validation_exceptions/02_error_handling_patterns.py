"""
Error Handling Patterns
=======================
Three shapes you will write over and over in real apps.
"""

from typing import Any

from pydantic import BaseModel, ValidationError


class SignupPayload(BaseModel):
    email: str
    age: int


# 1. Try/except -- boundary code (HTTP handler, CLI, background worker).
def handle_request(raw: dict) -> str:
    try:
        payload = SignupPayload.model_validate(raw)
    except ValidationError as e:
        # Surface a single user-friendly summary, log the structured detail.
        return f"Rejected ({e.error_count()} issues): {e.errors()[0]['msg']}"
    return f"Welcome {payload.email}"


print(handle_request({"email": "a@x.com", "age": "nope"}))


# 2. Safe-parse helper -- returns (model, errors) so callers avoid try/except.
# Pairs well with Go/Rust-style error-as-value code paths.
def safe_parse(model_cls, data) -> tuple[BaseModel | None, list[dict] | None]:
    try:
        return model_cls.model_validate(data), None
    except ValidationError as e:
        return None, e.errors()


model, errors = safe_parse(SignupPayload, {"email": "a@x.com", "age": 30})
print("ok:", model)
model, errors = safe_parse(SignupPayload, {"email": "a@x.com"})
print("errs:", errors)


# 3. API-style formatting -- reshape Pydantic errors into your own contract.
# Frontends usually want {field: message} keyed for per-input display.
def to_api_errors(e: ValidationError) -> dict[str, str]:
    out: dict[str, str] = {}
    for err in e.errors():
        # loc is a tuple -- join for nested fields like "address.zip_code".
        field = ".".join(str(p) for p in err["loc"]) or "_"
        out[field] = err["msg"]
    return out


try:
    SignupPayload.model_validate({"age": "x"})
except ValidationError as e:
    print(to_api_errors(e))
