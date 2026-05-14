# Continuous Operational Governance Intelligence Platform

SOC2 Operational Intelligence & Incident Governance System.

## Principles
1. Deterministic First
2. Event-Driven Architecture
3. Provider Agnostic
4. Evidence-Centric
5. Explainability Mandatory
6. Human-in-the-Loop

## Stack
- FastAPI
- Celery
- PostgreSQL
- Redis
- Qdrant
- MinIO
- Docker Compose
- Next.js Frontend

## Quickstart

```bash
docker-compose up -d
```

## Running Tests

```bash
poetry install
poetry run pytest tests/test_system.py
```
