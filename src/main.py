from typing import Iterator
from fastapi import FastAPI, HTTPException, status
import json
from sqlalchemy.orm.session import Session
from src.infrastructure.postgresql.database import SessionLocal
from src.interface.controller import api_router
import service
# config
app = FastAPI(__name__)

app.include_router(api_router, prefix="/api")


@app.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def healthz():
    return json.dumps({"message": "I am Zaemon."})
