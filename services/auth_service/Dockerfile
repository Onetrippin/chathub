FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.4 \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --only main --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn auth_service.wsgi:application -b 0.0.0.0:8000 --workers 2 --threads 4 --timeout 60"]
