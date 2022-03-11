from typing import Iterator
from fastapi import FastAPI, status
import json
from src.infrastructure.postgresql.database import SessionLocal
from src.interface.controller import api_router

# config
app = FastAPI(__name__)

app.include_router(api_router)


@app.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def healthz():
    return json.dumps({"message": "I am Zaemon."})
