from fastapi import (
    Body,
    Depends,
    FastAPI,
)

app = FastAPI()


# Part 24 - Sub-Dependencies
# There may be situations where you need to have multiple dependencies for a given path operation, but not 
#   necessarily side by side instead where one depends on another. 
# 
# Let's say, for example, that you want to see if a logged in user is active. 
# Well, you would need to have access to a database session as well as you would need
#  code that checks to see if the logged in user is active.

# same as we used in part 22

def query_extractor(q: str | None = None):
    return q


def query_or_body_extractor(
    q: str = Depends(query_extractor), last_query: str | None = Body(None)
):
    if q:
        return q
    return last_query


@app.post("/item")
async def try_query(query_or_body: str = Depends(query_or_body_extractor)):
    return {"q_or_body": query_or_body}
