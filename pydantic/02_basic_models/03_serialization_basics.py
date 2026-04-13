"""
Serialization Basics
====================
Turn models into dicts/JSON for outgoing payloads, logs, caches.

Methods
-------
m.model_dump()            →  dict          (logs, templates, jsonable_encoder)
m.model_dump_json()       →  str           (HTTP responses — faster than json.dumps)

Filters (all are kwargs to model_dump / model_dump_json)
--------------------------------------------------------
include={...}             →  whitelist   (safe public fields)
exclude={...}             →  blacklist   (strip secrets)
exclude_none=True         →  drop None   (PATCH / OpenAPI friendliness)
exclude_unset=True        →  only caller-provided fields   (PATCH diffs)
exclude_defaults=True     →  drop fields equal to default

Rule of thumb
-------------
Building a PATCH body?        → exclude_unset=True
Returning a public API model? → exclude={"password_hash", ...}
Sending over HTTP?            → model_dump_json()  (native datetime/UUID support)
"""

from pydantic import BaseModel


class Account(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str
    bio: str | None = None


acc = Account(id=42, username="alice", email="a@x.com",
              password_hash="sha256$abc...", bio=None)

print(acc.model_dump_json())                         # over the wire
print(acc.model_dump(exclude={"password_hash"}))     # strip secrets
print(acc.model_dump(exclude_none=True))             # drop bio=None


# exclude_unset shines for PATCH: only fields the caller actually set
# end up in the payload, so you don't accidentally overwrite with defaults.
partial = Account(id=1, username="bob", email="b@x.com", password_hash="x")
print(partial.model_dump(exclude_unset=True))
