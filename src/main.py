from fastapi import FastAPI, status
import json
from interface.controller import api_router
from command import make_superuser, create_tables

app = FastAPI()

app.include_router(api_router)

create_tables()

make_superuser()


@app.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def healthz():
    return {"message": "I am Zaemon."}
