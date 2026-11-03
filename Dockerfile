# syntax=docker/dockerfile:1

# --- Build Stage ---
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv \
    && pip install --no-cache-dir -U pip pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv requirements > requirements.txt \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# --- Runtime Stage ---
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE="popell_top100.prod_settings"

WORKDIR /project

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system --gid 10001 appuser \
    && useradd --system --uid 10001 --gid appuser --home-dir /project --no-create-home appuser

COPY --from=builder /opt/venv /opt/venv
COPY --chown=appuser:appuser . /project/

RUN mkdir -p /project/staticfiles \
    && chown -R appuser:appuser /project \
    && chmod +x /project/startup.sh

USER appuser

RUN DJANGO_SECRET="build-collectstatic-dummy-key" python manage.py collectstatic --noinput

EXPOSE 8000
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/accounts/login/', timeout=3)"]

CMD ["/project/startup.sh"]
