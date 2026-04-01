#!/bin/sh

PORT=${INNER_PORT:-8000}

alembic upgrade head
exec uvicorn main:app --host 0.0.0.0 --port $PORT