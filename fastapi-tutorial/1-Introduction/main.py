from fastapi import FastAPI
import asyncio

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post("/")
async def post():
    return {"message": "hello from the post route"}


@app.put("/")
async def put():
    return {"message": "hello from the put route"}


# ************************

async def asynchronous_operation():
    # Simulating an asynchronous operation
    await asyncio.sleep(1)
    return "Async operation complete"


@app.get("/async-route")
async def async_route():
    result = await asynchronous_operation()
    return {"message": result}
