FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/venv \
    PATH="/venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential default-libmysqlclient-dev pkg-config netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv $VIRTUAL_ENV

WORKDIR /app

COPY requirements.txt .
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip \
    && $VIRTUAL_ENV/bin/pip install -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' /app/entrypoint.sh || true

EXPOSE 8000