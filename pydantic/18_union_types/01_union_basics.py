"""
Union basics
============
A field that accepts more than one type. Pydantic v2 uses smart unions
by default -- it tries to pick the best match rather than left-to-right.
"""

from pydantic import BaseModel


class Lookup(BaseModel):
    # Accept either a numeric id or a slug -- common in REST APIs:
    # /users/42  or  /users/alice
    identifier: int | str


print(Lookup(identifier=42).identifier)       # 42  (int)
print(Lookup(identifier="alice").identifier)  # alice  (str)

# Smart mode keeps an int as int and a str as str instead of coercing
# "42" -> 42 just because int is listed first. That prevents silent
# data-shape changes between requests.
print(Lookup(identifier="42").identifier, type(Lookup(identifier="42").identifier))


# Union of models works too -- but ambiguous shapes should use a
# discriminated union (see next file) for speed and better errors.
class Email(BaseModel):
    address: str


class Phone(BaseModel):
    number: str


class Contact(BaseModel):
    via: Email | Phone


print(Contact(via={"address": "a@b.co"}))
print(Contact(via={"number": "+123"}))
