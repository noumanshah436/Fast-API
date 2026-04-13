"""
Attribute Access & Introspection
================================
Dot access for reads, model_fields for metadata, model_copy for updates.
"""

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str
    email: str = Field(description="Login email, case-insensitive")
    is_admin: bool = False


u = User(id=1, name="Alice", email="a@x.com")

# Plain attribute access -- same as any Python object.
print(u.name, u.email)


# model_fields exposes FieldInfo for every field: type, default, description, etc.
# Useful when building generic tooling (admin UIs, form generators, migrations).
for name, info in User.model_fields.items():
    print(f"{name}: required={info.is_required()} desc={info.description!r}")


# model_copy creates a new instance with selected fields replaced.
# Prefer this over mutating attributes -- keeps immutability semantics clean
# and avoids re-running full validation when you only tweak a known value.
promoted = u.model_copy(update={"is_admin": True})
print(promoted)
print(u.is_admin, promoted.is_admin)   # original untouched

# deep=True also copies nested models, not just the top-level.
clone = u.model_copy(deep=True)
print(clone == u, clone is u)
