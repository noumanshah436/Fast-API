"""
Serialization Basics
====================
model_dump / model_dump_json for outgoing payloads; filter with include/exclude.
"""

from pydantic import BaseModel


class Account(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str       # sensitive -- never return to clients
    bio: str | None = None


acc = Account(
    id=42,
    username="alice",
    email="a@x.com",
    password_hash="sha256$abc...",
    bio=None,
)

# dict form -- feed into logs, template contexts, or jsonable_encoder.
print(acc.model_dump())

# JSON string -- what you actually send over HTTP. Faster than json.dumps(dict)
# because Pydantic serializes types like datetime/UUID directly.
print(acc.model_dump_json())


# Whitelist: only fields safe to expose publicly.
print(acc.model_dump(include={"id", "username", "email"}))

# Blacklist: strip secrets before returning from an API.
print(acc.model_dump(exclude={"password_hash"}))


# exclude_none drops None fields -- handy when the consumer treats
# missing-vs-null differently (e.g., PATCH semantics, OpenAPI schemas).
print(acc.model_dump(exclude_none=True))

# exclude_unset returns only fields the caller actually set -- perfect for
# building PATCH requests where you must not overwrite with defaults.
partial = Account(id=1, username="bob", email="b@x.com", password_hash="x")
print(partial.model_dump(exclude_unset=True))
