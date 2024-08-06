
from fastapi import FastAPI, Query, Path

app = FastAPI()


@app.get("/items_hidden")
async def hidden_query_route(
    hidden_query: str | None = Query(None, include_in_schema=False)
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {"hidden_query": "Not found"}


@app.get("/items_validation/{item_id}")
async def read_items_validation(
    *,  # this says that any parameters after this are keyword arguments
    item_id: int = Path(..., title="The ID of the item to get", gt=10, le=100),
    q: str = "hello",
    size: float = Query(..., gt=0, lt=7.75)
):
    results = {"item_id": item_id, "size": size}
    if q:
        results.update({"q": q})
    return results


# Path is for Path parameters
# Query is for Query parameters
