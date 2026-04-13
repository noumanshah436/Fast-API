"""
Strict types and strict mode
============================
Three levers to turn coercion off. Pick the narrowest one that fits.

Scope          How                                      Use when
-----------------------------------------------------------------------------
per field      StrictInt / StrictStr / StrictBool /     Only a handful of
               StrictFloat                              safety-critical fields
per model      model_config = ConfigDict(strict=True)   Whole model is internal
per call       Model.model_validate(d, strict=True)     One trusted boundary
-----------------------------------------------------------------------------

Rules of thumb:
- Public HTTP / form endpoints       -> stay lax, users expect it.
- Money, auth, service-to-service    -> strict; a silent "10" -> 10 is a landmine.
- StrictBool is stricter than `bool` -- "true"/"false"/0/1 all REJECTED;
  only real True / False pass.
"""

from pydantic import BaseModel, ConfigDict, StrictBool, StrictInt, ValidationError


class Transfer(BaseModel):
    # Amounts and confirm flags must never be string-coerced. `note` can
    # stay lax -- padded whitespace there isn't a security issue.
    amount_cents: StrictInt
    confirmed: StrictBool
    note: str = ""


try:
    Transfer(amount_cents="1000", confirmed="true")
except ValidationError as e:
    # Each StrictX field fails independently -- one error entry per bad field.
    print("per-field rejected:", [err["loc"] for err in e.errors()])


class AuthRequest(BaseModel):
    # Model-wide strict seals every loophole: no "false" slipping in as True
    # for remember_me, no "7" sneaking through as an int user_id.
    model_config = ConfigDict(strict=True)
    user_id: int
    token: str
    remember_me: bool


try:
    AuthRequest(user_id="7", token="abc", remember_me="false")
except ValidationError as e:
    print("model-wide rejected:", len(e.errors()), "errors")
