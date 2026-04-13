"""
Correct pattern: default_factory
================================
Always use default_factory for mutable defaults -- explicit, portable, safe.
"""

from pydantic import BaseModel, Field


class Cart(BaseModel):
    # default_factory is called fresh for every new instance.
    # The factory is any zero-arg callable: list, dict, set, datetime.utcnow, ...
    items: list[str] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)
    tags: set[str] = Field(default_factory=set)


a = Cart()
b = Cart()
a.items.append("apple")
a.metadata["coupon"] = "SPRING10"

print(a.model_dump())
# {'items': ['apple'], 'metadata': {'coupon': 'SPRING10'}, 'tags': set()}

print(b.model_dump())
# {'items': [], 'metadata': {}, 'tags': set()}  -- totally independent


# Common real-world factories:
#   Field(default_factory=list)               -- empty collection
#   Field(default_factory=dict)
#   Field(default_factory=lambda: {"v": 1})   -- custom literal
#   Field(default_factory=uuid.uuid4)         -- unique id per row
#   Field(default_factory=datetime.utcnow)    -- created_at timestamps
