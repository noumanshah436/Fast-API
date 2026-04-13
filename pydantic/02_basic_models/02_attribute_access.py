"""
Attribute Access & Introspection
================================
Dot access for reads · model_fields for metadata · model_copy for updates.

Cheat sheet
-----------
u.name                         →  plain attribute read
User.model_fields              →  {name: FieldInfo}  for generic tooling
info.is_required()             →  required flag
info.description / default     →  docs & defaults (exposed in JSON Schema)
u.model_copy(update={...})     →  new instance with tweaks (no re-validation)
u.model_copy(deep=True)        →  also clones nested models

Why model_copy > mutation
-------------------------
- Keeps "value object" semantics (equality by content)
- Skips re-running full validation on every tweak
- Obvious at call sites: "here is a changed version", not "I mutated state"
"""

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str
    email: str = Field(description="Login email, case-insensitive")
    is_admin: bool = False


u = User(id=1, name="Alice", email="a@x.com")
print(u.name, u.email)


# Introspection — useful when building admin UIs, form generators, migrations.
for name, info in User.model_fields.items():
    print(f"{name}: required={info.is_required()} desc={info.description!r}")


# "Promote to admin" without touching the original — original stays untouched.
promoted = u.model_copy(update={"is_admin": True})
print(u.is_admin, promoted.is_admin)
# deep=True also copies nested models, not just the top-level.
clone = u.model_copy(deep=True)
print(clone == u, clone is u)
