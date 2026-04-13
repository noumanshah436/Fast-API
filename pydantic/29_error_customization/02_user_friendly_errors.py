"""
User-friendly error payloads
============================
Turn Pydantic's errors() list into {field: message} -- the shape
most frontends expect.
"""

from pydantic import BaseModel, EmailStr, ValidationError, field_validator


class RegisterForm(BaseModel):
    email: EmailStr
    age: int

    @field_validator("age")
    @classmethod
    def must_be_adult(cls, v: int) -> int:
        if v < 18:
            raise ValueError("You must be at least 18")
        return v


def flatten_errors(e: ValidationError) -> dict[str, str]:
    """Collapse ValidationError into {dotted.field: message} for API responses."""
    out: dict[str, str] = {}
    for err in e.errors():
        # loc is a tuple like ("address", "zip") -> "address.zip"
        field = ".".join(str(p) for p in err["loc"]) or "_root_"
        msg = err["msg"]
        # Strip the "Value error, " prefix Pydantic adds to ValueError messages.
        if msg.startswith("Value error, "):
            msg = msg[len("Value error, "):]
        out[field] = msg
    return out


try:
    RegisterForm(email="not-an-email", age=15)
except ValidationError as e:
    payload = flatten_errors(e)
    print(payload)
    # {'email': 'value is not a valid email address: ...', 'age': 'You must be at least 18'}


# Use flatten_errors in a FastAPI exception handler to return 422 with
# a consistent body across every endpoint.
