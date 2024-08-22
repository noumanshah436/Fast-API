from datetime import time, timedelta
from enum import Enum
import time

from fastapi import (
    FastAPI,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


# Part 28 - Middleware and CORS
class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

# my custom middleware
app.add_middleware(MyMiddleware)

# cors middleware
origins = ["http://localhost:8000", "http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins)


@app.get("/blah")
async def blah():
    return {"hello": "world"}
