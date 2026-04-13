# Constrained Types

Restrict values beyond just the type: length, range, pattern, multiples.

In Pydantic v2 the preferred style is `Annotated[T, Field(...)]`. The old
`constr` / `conint` / `confloat` helpers still work but are kept for
backward compatibility.

## Key takeaways
- Use `Annotated[str, Field(min_length=..., pattern=...)]` for strings.
- Use `Field(gt=, ge=, lt=, le=, multiple_of=)` for numerics.
- Constraints are validated at construction and on assignment (if enabled).
- Prefer `Annotated` — it composes with other validators cleanly.

## When / why
- Reject bad input at the edge (usernames, prices, quantities).
- Push invariants into the type, not scattered `if` checks.
- The JSON schema auto-reflects the constraints — free API docs.

## Files
| File | Topic |
|------|-------|
| 01_field_constraints.py | String constraints via `Annotated + Field` |
| 02_numeric_constraints.py | Numeric bounds and multiples |
| 03_legacy_con_types.py | Legacy `constr` / `conint` helpers |
