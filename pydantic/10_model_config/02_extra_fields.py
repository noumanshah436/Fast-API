"""
Extra fields policy
===================
What happens when input carries keys you didn't declare? You pick the policy.

Setting             Behavior                         When to use
---------------------------------------------------------------------------------
extra="ignore"      silently drop unknown keys       default; lenient readers
extra="forbid"      raise ValidationError            request bodies -- surface typos
extra="allow"       keep them as attributes          webhook envelopes, pass-through

Gotchas:
- `extra="ignore"` is the default -- clients can send garbage and you'll never know.
- `extra="forbid"` catches frontend field-name drift early (e.g. `userName` vs `username`).
- `extra="allow"` kept-keys also appear in `model_dump()` -- they become "real" data.
"""

from pydantic import BaseModel, ConfigDict, ValidationError


class IgnoreModel(BaseModel):
    # Default policy -- unknown keys vanish without a trace.
    model_config = ConfigDict(extra="ignore")
    id: int


class ForbidModel(BaseModel):
    # Strict contract -- any unexpected key raises `extra_forbidden`.
    # Best for inbound API payloads so typos don't silently no-op.
    model_config = ConfigDict(extra="forbid")
    id: int


class AllowModel(BaseModel):
    # Keep the extras -- model acts like a partially typed envelope.
    # Good fit: third-party webhooks where new fields appear over time.
    model_config = ConfigDict(extra="allow")
    id: int


payload = {"id": 1, "unexpected": "hello"}

print(IgnoreModel(**payload).model_dump())    # {'id': 1} -- 'unexpected' dropped

try:
    ForbidModel(**payload)
except ValidationError as e:
    print("forbid rejected:", e.errors()[0]["type"])   # 'extra_forbidden'

m = AllowModel(**payload)
print(m.model_dump())    # {'id': 1, 'unexpected': 'hello'} -- extras survive
print(m.unexpected)      # and are reachable as plain attributes
