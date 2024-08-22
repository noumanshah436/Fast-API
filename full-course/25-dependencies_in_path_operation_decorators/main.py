from fastapi import (
    Depends,
    FastAPI,
    Header,
    HTTPException,
)

app = FastAPI()


# Part 25 - Dependencies in path operation decorators

# There may be situations where you have multiple routes that all use the same dependencies and
# it's tedious to have to copy and paste the same code for each route.

# In these situations it would be helpful to be able to add dependencies to the APIRouter that you're using, or even to the entire FastAPI app as a whole.

# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


@app.get("/users/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


# We can put dependencies in our path oprator decorators if you don't need the values that they return.
# example:
#   @app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])


# If you need to work with the values that they return, we we'll put them in the path opration definations.
# example:
# async def read_items(key: str = Depends(verify_key)):
