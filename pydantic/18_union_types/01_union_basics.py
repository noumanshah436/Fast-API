"""
Union basics
============
A field that accepts more than one type. v2 is *smart*: exact-type match
beats left-to-right order, so `int | str` no longer silently turns "42" -> 42.

v1 behaviour                         v2 behaviour (default "smart")
-----------------------------------------------------------------
Left-to-right, first match wins.     Exact type match wins.
"42" for `int | str` -> 42 (int).    "42" stays "42" (str).

Gotchas:
- Prefer `X | Y` (PEP 604) over `Union[X, Y]` in v2.
- For model unions with a tag, use a discriminator (see 02_discriminated_union.py):
  faster dispatch AND clearer error messages than shape-matching every branch.
- Need the old behaviour? `Field(union_mode="left_to_right")`.
"""

from pydantic import BaseModel


class Lookup(BaseModel):
    # Supports /users/42 AND /users/alice on one endpoint (id or slug).
    identifier: int | str


print(Lookup(identifier=42).identifier)          # 42 (int)
print(Lookup(identifier="alice").identifier)     # 'alice' (str)
print(type(Lookup(identifier="42").identifier))  # <class 'str'> -- smart mode wins


class Email(BaseModel):
    address: str


class Phone(BaseModel):
    number: str


class Contact(BaseModel):
    # This works via shape-matching, but a discriminated union is clearer
    # and faster once there's a real `type` tag.
    via: Email | Phone


print(Contact(via={"address": "a@b.co"}))
print(Contact(via={"number": "+123"}))
