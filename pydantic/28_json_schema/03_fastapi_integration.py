"""
FastAPI integration
===================
Declaring a Pydantic model is the whole integration: FastAPI reads it to
parse requests, validate responses, publish /openapi.json, and render /docs.

What FastAPI does for each endpoint                    Powered by
--------------------------------------------------------------------------
Parse & validate request body                          model_validate_json
Return 422 with structured error list on bad input     ValidationError.errors()
Build /openapi.json for consumers                      model_json_schema()
Render Swagger UI at /docs                             same schema
Validate return value (response_model=...)             model_validate

No extra decorators, no hand-written YAML -- the type hints carry it.
"""

# Left as a comment-only example so this file runs without FastAPI installed.
# (Install FastAPI + uvicorn locally if you want to exercise it.)

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class User(BaseModel):
    # description + examples surface in /docs next to the field.
    id: int = Field(description="Primary key.", examples=[1])
    name: str = Field(description="Display name.", examples=["Alice"])

class UserCreate(BaseModel):
    # Separate input model -> never accept an id from the client.
    name: str

@app.post("/users", response_model=User)
def create_user(payload: UserCreate) -> User:
    # payload is already validated; inside the handler, trust the types.
    return User(id=1, name=payload.name)

# Gotcha: the handler's return value is re-validated against response_model.
# That's a feature -- it stops accidental leakage of extra fields.
