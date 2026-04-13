# 18. Union Types

## ⚡ TL;DR
`X | Y` accepts multiple types. v2 runs in **smart mode**: exact type match wins, no silent left-to-right coercion. For polymorphic payloads, add a discriminator.

## 🎯 When to use
- APIs that accept id-or-slug (`int | str`).
- Webhooks / event buses where payload shape depends on a `type` tag.
- Polymorphic DTOs (shipping vs pickup, card vs bank transfer, etc.).

## 🔧 Smart vs discriminated

| | Smart union (`A \| B`) | Discriminated (`Field(discriminator="type")`) |
|-|-------------------------|-----------------------------------------------|
| Dispatch | Try all members | Tag lookup (O(1)) |
| Errors | Lists every branch | Points at the tag mismatch |
| Schema | `anyOf` | `oneOf` with mapping |
| Needs `Literal` tag | No | Yes |

## ⚠️ Gotchas
- Prefer `A | B` over `Union[A, B]` in v2.
- Missing discriminator field -> startup-time error, not runtime surprise.
- Need v1 left-to-right behaviour? `Field(union_mode="left_to_right")`.

## Files
| File | Topic |
|------|-------|
| 01_union_basics.py | `X \| Y` unions + smart mode |
| 02_discriminated_union.py | `Field(discriminator=...)` for tagged payloads |
