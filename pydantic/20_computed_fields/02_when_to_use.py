"""
@computed_field vs plain @property
==================================
Both are read-only. Only @computed_field appears in dumps and schema.
"""

from pydantic import BaseModel, computed_field


class Box(BaseModel):
    width: float
    height: float
    depth: float

    # Plain @property: usable in code, hidden from serialization.
    # Good for internal helpers that clients don't need.
    @property
    def is_cube(self) -> bool:
        return self.width == self.height == self.depth

    # @computed_field: part of the public, serialized shape of the model.
    # Good for values API consumers should see.
    @computed_field
    @property
    def volume(self) -> float:
        return self.width * self.height * self.depth


b = Box(width=2, height=3, depth=4)
print(b.is_cube)          # False -- available on the instance
print(b.volume)           # 24.0
print(b.model_dump())     # {'width': 2.0, 'height': 3.0, 'depth': 4.0, 'volume': 24.0}
# Note: is_cube is absent from the dump.

# Rule of thumb:
# - Client should see it in JSON? -> @computed_field
# - Internal logic / helper only? -> plain @property
# - Needs to be settable / validated? -> make it a real field with a validator
