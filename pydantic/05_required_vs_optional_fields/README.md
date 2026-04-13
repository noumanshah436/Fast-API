# Topic 5: Required vs Optional Fields

## The Rule

In Pydantic, whether a field is **required** or **optional** depends entirely on whether it has a **default value**:

| Declaration | Required? | Explanation |
|-------------|-----------|-------------|
| `name: str` | Yes | No default -- must be provided |
| `name: str = "Unknown"` | No | Has a default value |
| `name: str = None` | No | Default is None (but type hint says str, so this is a bit loose) |
| `name: Optional[str]` | Yes | Optional means "str or None", but there's no default, so it's still required |
| `name: Optional[str] = None` | No | Accepts str or None, defaults to None |

## Common Confusion: Optional Does NOT Mean "Optional to Provide"

`Optional[str]` from the `typing` module means "this field can be `str` or `None`". It says nothing about whether you must provide a value. A field is only optional to provide if it has a default.

```python
class User(BaseModel):
    # Required -- must provide a value, and that value can be str or None
    nickname: Optional[str]

    # Not required -- if not provided, defaults to None
    bio: Optional[str] = None
```

## Ellipsis (...) for Explicit Required

You can use `...` (Ellipsis) with `Field()` to make it explicit that a field is required:

```python
from pydantic import Field

class User(BaseModel):
    name: str = Field(..., min_length=1)  # Required + has a constraint
```

## Files in This Section

| File | Description |
|------|-------------|
| `01_required_fields.py` | Fields without defaults, Ellipsis syntax |
| `02_optional_fields.py` | Optional type hint, default None, subtle distinctions |
| `03_default_values.py` | Static defaults, interaction with validation |
