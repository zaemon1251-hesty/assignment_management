#!/bin/sh

. /src/.venv/bin/activate
poetry run uvicorn main:app --host 0.0.0.0 --reload