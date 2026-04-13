"""
Leading-underscore fields
=========================
Names starting with `_` are treated as private -- same effect as PrivateAttr.
Use model_post_init to initialize them from field values.
"""

from pydantic import BaseModel, PrivateAttr


class Article(BaseModel):
    title: str
    body: str

    # Declared as a PrivateAttr because bare `_word_count: int = 0`
    # at class level would be rejected -- Pydantic needs to know it's private.
    _word_count: int = PrivateAttr(default=0)

    def model_post_init(self, __context) -> None:
        # Runs after validation, so self.body is the validated value.
        # Perfect place to derive / cache things on the instance.
        self._word_count = len(self.body.split())


a = Article(title="Hi", body="one two three four")
print(a._word_count)     # 4
print(a.model_dump())    # {'title': 'Hi', 'body': 'one two three four'}

# Set directly -- private attrs are regular mutable attributes, not validated.
a._word_count = 999
print(a._word_count)

# Tip: prefer PrivateAttr with an explicit default/default_factory. It's
# clearer than relying on the underscore convention alone, and plays
# nicely with type-checkers.
