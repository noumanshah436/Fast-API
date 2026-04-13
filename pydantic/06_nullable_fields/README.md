# Topic 6: Nullable Fields

## Nullable vs Optional-to-Provide

These are two independent axes that Pydantic keeps separate:

- **Nullable**: the field's **type** allows `None` as a value (`str | None`).
- **Optional to provide**: the field has a **default**, so callers can omit it.

A field can be any combination of the two. The type hint controls nullability; the presence of a default controls required-vs-optional.

| Declaration | Can be None? | Can be omitted? |
|-------------|--------------|-----------------|
| `name: str` | No | No |
| `name: str = "x"` | No | Yes |
| `name: str \| None` | Yes | No (must pass explicitly, even as None) |
| `name: str \| None = None` | Yes | Yes |

## Key Takeaways

- `str | None` (or `Optional[str]`) only widens the **type**; it does not make the field optional to provide.
- To make a field both nullable AND omittable, add `= None`.
- Use "required-nullable" (`x: str | None`) when the API contract says the client must acknowledge the field -- even to clear it. Useful for PATCH-style updates where omitted means "leave alone" and `null` means "clear".
- Use "optional-nullable" (`x: str | None = None`) for truly optional values like profile bios, nicknames, trailing metadata.

## When to Use

- **DB models** mirroring a nullable column: `str | None = None` if inserts may omit it, `str | None` without a default if you always pass it.
- **PATCH request bodies**: required-nullable gives you the omit/null distinction needed to implement "don't touch" vs "set to null".
- **Config loaders**: almost always `Type | None = None` for optional settings.

## Files in This Section

| File | Description |
|------|-------------|
| `01_allowing_none.py` | `str \| None` accepts None as a valid value |
| `02_optional_vs_nullable.py` | required-nullable vs optional-nullable, PATCH pattern |
