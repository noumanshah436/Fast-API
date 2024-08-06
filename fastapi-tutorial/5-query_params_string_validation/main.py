
from fastapi import FastAPI, Query

app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/

#  we can use Optional[str] instead of (str | None )

# ******************************

# syntax
# Query(default_value, other_options)

# ******************************

# Query(..., other_options)
# it says says that it do not have any default value, but it is required

# ******************************

# it says that q should be the list if strings, and the default value is ["str1", "str2"]
# def read_items(q: list(str) = Query(["str1", "str2"])

# ******************************



@app.get("/items")
async def read_items(
    q: str | None = Query(
        None,
        min_length=3,
        max_length=10,
        title="Sample query string",
        description="This is a sample query string.",
        alias="item-query",  # now we need to pass this query parameter as item-query
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items_hidden")
async def hidden_query_route(
    hidden_query: str | None = Query(None, include_in_schema=False)
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {"hidden_query": "Not found"}
