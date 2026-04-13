"""
Field aliases
=============
Bridge the wire format (camelCase JSON) and Python (snake_case).

Kind                 Controls           Example
---------------------------------------------------------------
alias                input AND output   alias="firstName"
validation_alias     input only         accept "fname" on the way IN
serialization_alias  output only        emit "first_name" on the way OUT
populate_by_name     also accept the Python name alongside the alias

Defaults you usually want:
  ConfigDict(populate_by_name=True)     # tolerant input
  model_dump(by_alias=True)             # emit wire format

Gotcha: without populate_by_name, constructing with the Python name raises.
"""

from pydantic import BaseModel, ConfigDict, Field


class UserProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    signup_ts: int = Field(..., alias="signupTs")


# Incoming JS/TS payload.
u = UserProfile(**{"firstName": "Ada", "lastName": "Lovelace", "signupTs": 1700000000})
print(u.first_name)

# Python-native construction still works thanks to populate_by_name.
u2 = UserProfile(first_name="Grace", last_name="Hopper", signup_ts=1700000001)
print(u2.model_dump(by_alias=True))   # emit camelCase back to the client
