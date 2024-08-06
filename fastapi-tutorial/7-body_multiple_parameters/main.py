
from fastapi import FastAPI, Path, BaseModel, Body


app = FastAPI()


# Part 7 -> Body - Multiple Parameters
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=150),
    q: str | None = None,
    item: Item = Body(..., embed=True),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# ************************************

# accept the username and password as body parameters:

# username: str = Body(...),
# password: str = Body(...),

# *************************************

# item: Item = Body(..., embed=True), 

# If we set embed=True, then we need to pass Body params wrapped in key value pairs like

# {
#     'items': {
#         'name': 'Foo',
#         'description': 'A sample item',
#         'price': 19.99,
#         'tax': 10.0
#     }
# }