"""
include / exclude
=================
Shape the output -- hide secrets, build PATCH bodies, trim nulls.

Option              Keeps in output
------------------------------------------------------------------
include={"a", "b"}  only listed fields (whitelist)
exclude={"pwd"}     everything except listed fields (blacklist)
exclude_none=True   drops fields whose value is None
exclude_unset=True  drops fields the caller never set (PATCH gold)
exclude_defaults=T  drops fields still at their default value

Nested form: include={"address": {"city"}}  -- same for exclude.

Rule of thumb:
- Response bodies  → exclude={"password_hash", ...}
- PATCH payloads   → exclude_unset=True
- Sparse public JSON → exclude_none=True
"""

from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    password_hash: str
    bio: str | None = None


u = User(id=1, email="a@x.com", password_hash="xxx")

print(u.model_dump(exclude={"password_hash"}))  # strip secrets before sending
print(u.model_dump(include={"id", "email"}))    # whitelist public fields
print(u.model_dump(exclude_none=True))          # 'bio' dropped

# exclude_unset shines for PATCH: only fields the caller actually set come out.
print(u.model_dump(exclude_unset=True))
