"""
Field aliases
=============
Bridge external camelCase JSON and internal snake_case Python.
"""

from pydantic import BaseModel, ConfigDict, Field


class UserProfile(BaseModel):
    # populate_by_name lets us use EITHER the alias or the field name as input.
    model_config = ConfigDict(populate_by_name=True)

    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    # serialization_alias would control output; alias covers both by default.
    signup_ts: int = Field(..., alias="signupTs")


# Typical API payload from a JS client (camelCase).
payload = {"firstName": "Ada", "lastName": "Lovelace", "signupTs": 1700000000}
u = UserProfile(**payload)
print(u.first_name)  # snake_case on the Python side

# populate_by_name=True also allows Python-native construction.
u2 = UserProfile(first_name="Grace", last_name="Hopper", signup_ts=1700000001)
print(u2.model_dump(by_alias=True))  # emit camelCase back out for the client
