"""
mode="before" vs mode="after"
=============================
"before" shapes the raw input; "after" polices the typed value.

Cheat sheet
---------------------------------------------------------------------------
mode="before"   v is the RAW caller input (str, list, None, ...)
                use it to RESHAPE: trim, split CSV, coerce, None→default
mode="after"    v is already the declared type (list[str] here)
                use it for DOMAIN RULES: lowercase, dedupe, range checks

Rule of thumb
- Use "before" ONLY to reshape input.
- Keep every semantic rule in "after" -- safer, clearer, type-guaranteed.
"""

from pydantic import BaseModel, field_validator


class Article(BaseModel):
    title: str
    # User submits "python, fastapi, pydantic" from a form; we want list[str].
    tags: list[str]

    # BEFORE: `v` is whatever the caller passed (str, list, None, ...).
    # Convert CSV -> list so the downstream type check succeeds.
    @field_validator("tags", mode="before")
    @classmethod
    def _split_csv(cls, v):
        if isinstance(v, str):
            return [t.strip() for t in v.split(",") if t.strip()]
        return v

    # AFTER: type is guaranteed list[str]; enforce a domain rule.
    @field_validator("tags", mode="after")
    @classmethod
    def _lowercase_unique(cls, v: list[str]) -> list[str]:
        seen, out = set(), []
        for tag in (t.lower() for t in v):
            if tag not in seen:
                seen.add(tag)
                out.append(tag)
        return out


print(Article(title="hi", tags="Python, FastAPI, python"))
# tags=['python', 'fastapi']  -- split, lowercased, deduped.

print(Article(title="hi", tags=["A", "b", "A"]))
# tags=['a', 'b']
