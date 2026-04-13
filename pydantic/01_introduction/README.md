# 1. Introduction to Pydantic

Pydantic is a **data validation** library powered by Python type hints.
You declare the shape of your data once; Pydantic parses, validates, and serializes it.

## Key Takeaways
- Validates runtime data against type hints (unlike plain dataclasses / TypedDict).
- Coerces compatible types (e.g., `"25"` -> `25`).
- Raises `ValidationError` with a JSON-friendly error list on bad input.
- Pydantic **v2** is a Rust-powered rewrite: much faster, new APIs (`model_dump`, `model_validate`).
- Engine behind **FastAPI** request/response models.

## When to Use It
- Parsing untrusted input: JSON APIs, webhooks, config files, CLI args.
- Defining the boundary between "raw data" and "typed objects" in your app.
- Anywhere you'd otherwise write manual `isinstance` / `try/except` validation.

## Files
- `01_what_is_pydantic.py` – minimal example + why it exists.
- `02_pydantic_vs_dataclasses.py` – validation is the differentiator.
- `03_v1_vs_v2.py` – API renames you will hit in old tutorials.
