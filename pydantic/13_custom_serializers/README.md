# 13. Custom Serializers

⚡ **TL;DR** — `@field_serializer` controls how `model_dump()` / `model_dump_json()` emit a field. Reach for it whenever the default representation doesn't match your API contract.

## 🎯 When to use

| Need                           | Example                                           |
|--------------------------------|---------------------------------------------------|
| Fixed `datetime` format        | ISO `YYYY-MM-DDTHH:MM:SSZ`, epoch seconds         |
| `Decimal` precision in JSON    | Emit as `str` so clients don't lose cents         |
| Enum human-friendly            | Emit `.name` ("ADMIN") instead of `.value`        |
| Mask sensitive data            | `****1234` for card / SSN fields                  |
| Different dict vs JSON         | `when_used="json"` keeps Python dict raw          |

## Serializer modes

| Decorator option               | Behavior                                          |
|--------------------------------|---------------------------------------------------|
| `@field_serializer("x")`       | Runs for both dict + JSON output                  |
| `when_used="json"`             | Only customizes `model_dump_json`                 |
| `when_used="unless-none"`      | Skips `None` values                               |
| `@field_serializer("x", "y")`  | Share one function across fields                  |
| `@field_serializer("*")`       | Apply to every field (wildcard)                   |

## ⚠️ Gotchas

- Serializers **only** run on output — they don't affect validation.
- `Decimal` becomes `float` by default in JSON — always serialize to `str` for money.
- `use_enum_values=True` in `ConfigDict` is a shortcut for always-value output.

## Files

| File                      | What it shows                                      |
|---------------------------|----------------------------------------------------|
| `01_field_serializer.py`  | `datetime` + `Decimal` custom formatting           |
| `02_serializing_enums.py` | Default value output vs `.name` output             |
