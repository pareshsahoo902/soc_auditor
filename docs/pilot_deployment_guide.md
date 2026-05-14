# Pilot Deployment Guide

## Overview
This guide provides instructions for deploying the SOC2 Operational Intelligence Platform for a pilot customer.

## Prerequisites
- Docker & Docker Compose
- API Keys for Jira, GitHub, Zendesk, Confluence (if integrating live)
- Groq API Key (for AI Enrichment)

## Setup Steps
1. Clone the repository.
2. Configure `.env` with necessary secrets (use `shared/configs/settings.py` as reference).
3. Run `docker-compose up -d`.
4. Access the API at `http://localhost:8000/docs` and the Dashboard at `http://localhost:3000`.

## Integration
- Point Jira webhooks to `/api/v1/webhooks/jira`
- Point GitHub webhooks to `/api/v1/webhooks/github`

## Evaluation
Monitor false positives and AI extraction accuracy using the built-in golden dataset evaluation framework (to be executed via tests).
