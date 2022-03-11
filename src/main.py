from typing import Iterator
from fastapi import FastAPI, status
import json
from interface.controller import api_router
from domain import AuthedUser
# config
app = FastAPI(__name__)

app.include_router(api_router)


@app.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def healthz():
    return json.dumps({"message": "I am Zaemon."})
