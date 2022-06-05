from fastapi import FastAPI, status
import json
from src.settings import logger
from src.interface.controller import api_router

app = FastAPI()

app.include_router(api_router)


@app.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def healthz():
    return {"message": "I am Zaemon."}
