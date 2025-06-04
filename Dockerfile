ARG PYTHON_VERSION=3.13
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim AS base
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
WORKDIR /app

FROM base AS deps
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

FROM python:${PYTHON_VERSION}-slim-bookworm AS prod
WORKDIR /app
COPY src src
COPY models models
COPY *.env .
COPY --from=deps /app/.venv .venv

RUN . .venv/bin/activate
ENTRYPOINT []
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 50051
CMD ["python", "-m", "src"]
