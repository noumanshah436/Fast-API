"""
Error Handling Patterns
=======================
Three shapes you will write over and over.

1. try/except                  → boundary code (HTTP handler, CLI, worker)
2. safe_parse (model, errors)  → Go/Rust-style result tuples, no try/except at callers
3. to_api_errors {field: msg}  → frontend-friendly per-input display

Tip
---
Pydantic errors have nested `loc` tuples. For frontend JSON, join them:
    ("address", "zip_code")  →  "address.zip_code"
"""

from pydantic import BaseModel, ValidationError


class SignupPayload(BaseModel):
    email: str
    age: int


# 1. Boundary handler — log structured detail, return friendly summary.
def handle_request(raw: dict) -> str:
    try:
        payload = SignupPayload.model_validate(raw)
    except ValidationError as e:
        return f"Rejected ({e.error_count()} issues): {e.errors()[0]['msg']}"
    return f"Welcome {payload.email}"


# 2. Result-tuple helper — callers branch on `errors is None`.
def safe_parse(model_cls, data):
    try:
        return model_cls.model_validate(data), None
    except ValidationError as e:
        return None, e.errors()


# 3. Reshape into the frontend's contract: {field: first-message}.
def to_api_errors(e: ValidationError) -> dict[str, str]:
    return {".".join(str(p) for p in err["loc"]) or "_": err["msg"]
            for err in e.errors()}


print(handle_request({"email": "a@x.com", "age": "nope"}))
print(safe_parse(SignupPayload, {"email": "a@x.com"}))
try:
    SignupPayload.model_validate({"age": "x"})
except ValidationError as e:
    print(to_api_errors(e))
