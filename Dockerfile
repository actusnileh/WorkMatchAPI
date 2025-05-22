ARG PYTHON_VERSION=3.13.3

FROM python:${PYTHON_VERSION}-slim-bullseye AS builder

WORKDIR /work_match_api

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

RUN apt update -y && \
    apt install -y --no-install-recommends python3-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

FROM python:${PYTHON_VERSION}-slim-bullseye

WORKDIR /work_match_api

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local

ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

COPY . .
