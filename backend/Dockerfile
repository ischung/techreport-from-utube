# Backend — FastAPI + uv, Python 3.11-slim
# Single-stage: install deps, copy source, run uvicorn.

FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_LINK_MODE=copy

# Install uv (static binary) — pin to a known-good minor for reproducibility
RUN pip install --no-cache-dir uv==0.4.*

WORKDIR /app

# Install dependencies first for layer caching
COPY pyproject.toml ./
# uv.lock is optional until a lockfile lands
COPY uv.lock* ./

RUN uv sync --no-dev || uv pip install --system -e .

# Now copy the rest of the source
COPY app ./app

# Non-root user
RUN useradd --system --create-home --shell /usr/sbin/nologin app \
    && chown -R app:app /app
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/').read()" || exit 1

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
