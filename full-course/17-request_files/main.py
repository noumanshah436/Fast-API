from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal, Union
from uuid import UUID

from fastapi import (
    Body,
    FastAPI,
    Query,
    Path,
    Cookie,
    Header,
    status,
    Form,
    File,
    UploadFile,
)
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from starlette.responses import HTMLResponse

app = FastAPI()


# Part 17 - Request Files
@app.post("/files/")
async def create_file(
    files: list[bytes] = File(..., description="A file read as bytes")
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfile/")
async def create_upload_file(
    files: list[UploadFile] = File(...,
                                   description="A file read as UploadFile")
):
    return {"filename": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
