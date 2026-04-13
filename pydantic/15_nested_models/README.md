# 15. Nested Models

Pydantic models compose: a field can be another `BaseModel`, or a `list[...]`
of them. Validation and serialization both recurse automatically -- no manual
wiring required.

## Key Takeaways
- Nested dicts in the input are deep-validated into nested model instances.
- `list[Model]` / `dict[str, Model]` work the same way -- recursion all the way.
- `model_dump()` / `model_dump_json()` produce nested dict / JSON output.
- `Model.model_validate(json_list)` parses a top-level JSON array when you
  wrap it: `TypeAdapter(list[Model]).validate_python(...)`.

## When to Use It
- Any realistic API payload: `Order { customer, items[] }`, `User { address }`.
- Mapping relational data (FKs, joins) into a single request/response model.
- Pagination wrappers (`Page[Item]`).

## Files
- `01_nested_models.py` -- Order with Customer and Items.
- `02_list_of_models.py` -- parsing a JSON list of users.
- `03_nested_serialization.py` -- nested output via `model_dump`.
