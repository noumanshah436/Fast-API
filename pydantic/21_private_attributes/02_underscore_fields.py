"""
Underscore names + model_post_init
==================================
Names starting with `_` are treated as private. `model_post_init` runs AFTER
field validation, so it's the right place to derive values from validated data.

Ways to declare private state
-----------------------------
Form                                         Behaviour
--------------------------------------------------------------------
`_x: int = PrivateAttr(default=0)`           preferred — explicit + typed
`_x: int = PrivateAttr(default_factory=list)` per-instance mutable default
bare `_x = 0`                                 REJECTED — Pydantic requires PrivateAttr

model_post_init hook:
- Called once fields are validated; `self.<field>` is the clean value
- Perfect for caches, counts, hashes, or lazy resources keyed off fields
- Assigning to private attrs never triggers validation

Gotchas:
- Private attrs ignore `frozen=True` — a frozen model can still mutate them
- Type-checkers only "see" the attribute via the `PrivateAttr` annotation
"""

from pydantic import BaseModel, PrivateAttr


class Article(BaseModel):
    title: str
    body: str

    _word_count: int = PrivateAttr(default=0)

    def model_post_init(self, __context) -> None:
        # Runs post-validation -- safe to read self.body directly.
        self._word_count = len(self.body.split())


a = Article(title="Hi", body="one two three four")
print(a._word_count)         # 4 -- populated by the hook
print(a.model_dump())        # word count is NOT serialized

# Assignments to private attrs bypass validation entirely.
a._word_count = 999
print(a._word_count)
