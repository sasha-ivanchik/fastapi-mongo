#!/bin/bash
#alembic revision --autogenerate
alembic upgrade head
gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app --reload -b 0.0.0.0:8001
