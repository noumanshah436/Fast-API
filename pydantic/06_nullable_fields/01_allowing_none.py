"""
Allowing None
=============
Widen the type with `| None` (or Optional[X]) to accept nulls.
"""

from pydantic import BaseModel, ValidationError


class DBUser(BaseModel):
    # Mirrors a NOT NULL column -- None is rejected.
    id: int
    email: str

    # Mirrors a NULLABLE column -- None is a valid, meaningful value.
    # Think "user hasn't verified yet" or "deleted timestamp not set".
    verified_at: str | None
    deleted_at: str | None = None   # nullable AND omittable


# None is accepted where the type allows it.
u = DBUser(id=1, email="a@x.com", verified_at=None)
print(u.model_dump())

# And actual strings are still fine -- `str | None` means either.
u2 = DBUser(id=2, email="b@x.com", verified_at="2025-01-01T10:00:00")
print(u2.verified_at)


# None is rejected on a non-nullable field -- catches silent data corruption
# from upstream systems that think "no value" and None are interchangeable.
try:
    DBUser(id=3, email=None, verified_at=None)
except ValidationError as e:
    print(e.errors()[0]["type"])   # string_type


# deleted_at omitted -> defaults to None (omittable + nullable).
print(DBUser(id=4, email="c@x.com", verified_at=None).deleted_at)
