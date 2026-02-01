FROM python:3.12.11

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock start_backend.sh alembic.ini ./

RUN uv sync --locked

COPY ./src /app/src

RUN chmod +x /app/start_backend.sh