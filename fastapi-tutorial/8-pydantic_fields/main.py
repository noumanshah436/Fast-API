
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


# Part 8 -> Body - Fields
class Item(BaseModel):
    name: str
    description: str | None = Field(None, title="The description of the item", max_length=300)
    price: float = Field(..., gt=0, description="The price must be greater than zero.")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


# In FastAPI, `Field` and `Query` are used to define and validate input parameters, but they are used in different contexts.

# ### `Field` in FastAPI
# `Field` is used for defining metadata, validation, and default values for the fields in Pydantic models.
# Pydantic models are used for request bodies in FastAPI.

# #### Usage of `Field`
# ```python
# from pydantic import BaseModel, Field

# class Item(BaseModel):
#     name: str = Field(..., title="The name of the item", max_length=300)
#     description: str = Field(None, title="The description of the item", max_length=300)
#     price: float = Field(..., gt=0, description="The price must be greater than zero")
# ```

# ### `Query` in FastAPI
# `Query` is used to define metadata, validation, and default values for query parameters in your API endpoints. Query parameters are the parameters that are included in the URL.

# #### Usage of `Query`
# ```python
# from fastapi import FastAPI, Query

# app = FastAPI()

# @app.get("/items/")
# async def read_items(q: str = Query(None, min_length=3, max_length=50, regex="^fixedquery$")):
#     return {"q": q}
# ```

# Differences Between `Query` and `Field`

# 1. **Context of Use**:
#    - **`Field`**: Used inside Pydantic models to define and validate request body fields.
#    - **`Query`**: Used in function parameters to define and validate query parameters.

# 2. **Purpose**:
#    - **`Field`**: Primarily for request body validation and metadata in Pydantic models.
#    - **`Query`**: Primarily for query parameters in URL endpoints.

# 3. **Syntax and Functionality**:
#    - **`Field`**: Comes from Pydantic and is used to provide additional validation and metadata for the fields in Pydantic models.
#    - **`Query`**: Comes from FastAPI and is used to provide additional validation and metadata for the query parameters in API endpoints.

# ### Example to Illustrate the Difference

# #### Using `Field` with Pydantic Model
# ```python
# from fastapi import FastAPI
# from pydantic import BaseModel, Field

# app = FastAPI()

# class Item(BaseModel):
#     name: str = Field(..., title="The name of the item", max_length=300)
#     description: str = Field(None, title="The description of the item", max_length=300)

# @app.post("/items/")
# async def create_item(item: Item):
#     return item
# ```
# - **Request Body**: The `Item` object with `name` and `description` fields.

# #### Using `Query` for Query Parameters
# ```python
# from fastapi import FastAPI, Query

# app = FastAPI()

# @app.get("/items/")
# async def read_items(q: str = Query(None, min_length=3, max_length=50, regex="^fixedquery$")):
#     return {"q": q}
# ```
# - **Query Parameter**: `q` parameter in the URL with validation.

# ### Conclusion
# - Use `Field` within Pydantic models to define and validate the structure and content of request bodies.
# - Use `Query` in endpoint function parameters to define and validate query parameters.
