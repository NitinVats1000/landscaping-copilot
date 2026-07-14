# Production image. Built with uv so the install is reproducible from uv.lock.
FROM python:3.12-slim

# Grab the uv binary from its official image — no pip bootstrap needed.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 1) Dependencies FIRST, on their own layer.
#    Docker caches this layer and only rebuilds when the lockfile changes —
#    so a code-only change redeploys in seconds instead of minutes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# 2) Then the application code.
COPY . .
RUN uv sync --frozen --no-dev

# --no-dev = pytest/ruff/mypy are NOT in the production image.
# This is why we split app-deps from dev-deps back in Phase 2.

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src"

# Render injects PORT at runtime. Two things MUST be right:
#   --host 0.0.0.0  (NOT 127.0.0.1 — that only accepts traffic from inside the
#                    container, so Render's load balancer can never reach you.
#                    Classic "deploy succeeds but the URL 502s" bug.)
#   --port $PORT    (assigned by Render, never hardcoded)
# Migrations do NOT run here — they run as Render's Pre-Deploy Command, so only ONE
# process migrates (no race between container instances), and a failed migration is
# reported as a failed migration rather than a crashed app.
CMD uvicorn copilot.main:app --host 0.0.0.0 --port ${PORT:-8000}

