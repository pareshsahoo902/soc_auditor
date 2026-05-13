FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . .

CMD ["celery", "-A", "apps.worker.celery_app", "worker", "-Q", "ingestion_queue,extraction_queue,governance_queue,reporting_queue", "--loglevel=info"]
