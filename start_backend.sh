#!/bin/bash

printf "Run migrations:\n"
uv run alembic upgrade head

printf "Start backend:\n"
cd src || exit 1
uv run python main.py