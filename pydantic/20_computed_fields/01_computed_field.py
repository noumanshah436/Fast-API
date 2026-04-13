"""
@computed_field
===============
Derived, read-only values that appear in the serialized output.
"""

from pydantic import BaseModel, computed_field


class Person(BaseModel):
    first_name: str
    last_name: str

    # @computed_field tells Pydantic: include this in model_dump() and
    # the JSON schema. Without it, it'd be a regular property, invisible
    # to serialization. Always pair with @property.
    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


p = Person(first_name="Ada", last_name="Lovelace")
print(p.full_name)           # Ada Lovelace
print(p.model_dump())        # includes 'full_name'
print(p.model_dump_json())   # same in JSON


class Line(BaseModel):
    price: float
    quantity: int

    # Good fit: total is always priceXquantity, clients should never send it.
    @computed_field
    @property
    def total(self) -> float:
        return round(self.price * self.quantity, 2)


print(Line(price=9.99, quantity=3).model_dump())
