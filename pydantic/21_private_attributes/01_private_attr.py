"""
PrivateAttr — internal per-instance state
=========================================
Runtime state that lives OUTSIDE Pydantic's field machinery: skipped by
validation, hidden from dumps, invisible in the JSON schema.

PrivateAttr vs Field
--------------------
Aspect              PrivateAttr              Field
-------------------------------------------------------------
Validation          skipped                  runs
model_dump()        excluded                 included
JSON schema         excluded                 included
Constructor kwarg   silently ignored         accepted
Assignment          always allowed           blocked if frozen
Name convention     leading `_`              any

Good fits:
- Caches / memoized values / lazy clients (DB sessions, HTTP clients)
- Counters, internal flags, timestamps that must not hit the wire
- Anything that should NOT survive a JSON round-trip

Gotchas:
- Always pass `default=` or `default_factory=` — `PrivateAttr()` alone has no value
- `default_factory` runs per instance; NEVER share a mutable default
- `Model(_calls=5)` is ignored — private attrs aren't real fields
"""

from pydantic import BaseModel, PrivateAttr


class Counter(BaseModel):
    name: str

    # Private because callers shouldn't read/write these over the API surface.
    _calls: int = PrivateAttr(default=0)
    _cache: dict = PrivateAttr(default_factory=dict)  # fresh dict per instance

    def hit(self, key: str) -> int:
        self._calls += 1
        self._cache[key] = self._cache.get(key, 0) + 1
        return self._cache[key]


c = Counter(name="requests")
c.hit("a"); c.hit("a"); c.hit("b")
print(c._calls, c._cache)            # 3 {'a': 2, 'b': 1}

# Not present in public views -- privacy is enforced by the framework.
print(c.model_dump())                # {'name': 'requests'}
print(list(c.model_json_schema()["properties"]))  # ['name']

# Passing a private attr at construction is a silent no-op.
c2 = Counter(name="x", _calls=999)
print(c2._calls)                     # 0, not 999 -- proves kwargs were dropped
