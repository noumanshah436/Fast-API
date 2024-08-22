from fastapi import (
    Depends,
    FastAPI,
)

app = FastAPI()

# In the last video I showed you how to use a basic method as a dependency in a FastAPI app.
# Since python classes themselves are callable (in the way that you can instantiate an object of a class by adding parentheses after the name)
#    you are able to use python classes as dependencies as well.


# Part 23 - Classes as Dependencies
fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/{item_id}")
async def read_items(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    # index slicing here like arr[start:end]
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return response


# These are different ways to add dependencies, all these do the same thing:

# 1) async def read_items(commons: CommonQueryParams = Depends()):

# 2) async def read_items(commons: = Depends(CommonQueryParams)):

# 3) async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
