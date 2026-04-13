"""
PrivateAttr
===========
Internal per-instance state -- not validated, not serialized, not in schema.
"""

from pydantic import BaseModel, PrivateAttr


class Counter(BaseModel):
    name: str

    # default_factory runs per instance -- never share a mutable default.
    # _calls is a runtime counter, nothing the API should see or accept.
    _calls: int = PrivateAttr(default=0)
    _cache: dict = PrivateAttr(default_factory=dict)

    def hit(self, key: str) -> int:
        self._calls += 1
        self._cache.setdefault(key, 0)
        self._cache[key] += 1
        return self._cache[key]


c = Counter(name="requests")
c.hit("a"); c.hit("a"); c.hit("b")
print(c._calls, c._cache)   # 3 {'a': 2, 'b': 1}

# Private attrs are stripped from serialization and schema.
print(c.model_dump())        # {'name': 'requests'}
print(c.model_json_schema()["properties"].keys())  # only 'name'

# Passing them as constructor input is silently ignored -- they're
# not fields. Use them from within methods instead.
c2 = Counter(name="x", _calls=999)
print(c2._calls)   # 0, not 999
