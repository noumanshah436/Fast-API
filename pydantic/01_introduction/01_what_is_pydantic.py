"""
What is Pydantic?
=================
Runtime validation powered by Python type hints. Declare once, parse forever.

The pipeline
------------
raw input  →  Pydantic  →  typed object   (or ValidationError)
 dict/JSON     BaseModel    model instance

What you get
------------
- Parse:    dict / JSON / kwargs → typed model
- Coerce:   "1" → 1 · 1 → True · "2025-01-01" → date  (lax by default)
- Reject:   ValidationError with loc / msg / type / input
- Emit:     JSON + JSON Schema (FastAPI docs are built on this)

Where to put it
---------------
Use at app BOUNDARIES:  HTTP bodies · webhooks · configs · CLI args · DB rows.
Inside trusted code?    Use @dataclass — validation is wasted work there.
"""

from pydantic import BaseModel, ValidationError


class User(BaseModel):
    id: int
    name: str
    is_active: bool = True


# Lax coercion is intentional: form/query/JSON payloads "just work"
# without manual casting. "1" becomes 1, 1 becomes True.
u = User(id="1", name="Alice", is_active=1)
print(u.model_dump())


try:
    User(id="not-a-number", name="Bob")
except ValidationError as e:
    # .errors() -> list[dict], JSON-serializable, drop-in for 422 responses.
    print(e.errors()[0])
