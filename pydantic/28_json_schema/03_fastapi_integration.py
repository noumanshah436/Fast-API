"""
FastAPI integration
===================
FastAPI reads Pydantic models to build request/response schemas,
/openapi.json, and the Swagger UI at /docs -- for free.
"""

# Comment-only example so this file runs without FastAPI installed.
#
# from fastapi import FastAPI
# from pydantic import BaseModel, Field
#
# app = FastAPI()
#
# class User(BaseModel):
#     id: int = Field(description="Primary key.", examples=[1])
#     name: str = Field(description="Display name.", examples=["Alice"])
#
# class UserCreate(BaseModel):
#     name: str
#
# @app.post("/users", response_model=User)
# def create_user(payload: UserCreate) -> User:
#     # payload is already validated by the time we get here.
#     return User(id=1, name=payload.name)
#
# What FastAPI does behind the scenes:
# - Calls UserCreate.model_validate_json(request_body) -> 422 on error.
# - Calls User.model_json_schema() -> injects into /openapi.json.
# - Renders Swagger UI at /docs using that schema (descriptions, examples, types).
# - Validates the return value against response_model=User before serializing.
#
# Takeaway: the moment you declare a Pydantic model, FastAPI already knows
# how to parse it, document it, and generate a client for it.
