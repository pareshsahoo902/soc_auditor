from fastapi import APIRouter, Request
from services.jira_connector.client import JiraConnector
from services.github_connector.client import GitHubConnector
from services.zendesk_connector.client import ZendeskConnector
from services.confluence_connector.client import ConfluenceConnector

router = APIRouter()

@router.post("/webhooks/jira")
async def jira_webhook(request: Request):
    payload = await request.json()
    return JiraConnector().ingest_webhook(payload)

@router.post("/webhooks/github")
async def github_webhook(request: Request):
    payload = await request.json()
    return GitHubConnector().ingest_webhook(payload)

@router.post("/webhooks/zendesk")
async def zendesk_webhook(request: Request):
    payload = await request.json()
    return ZendeskConnector().ingest_webhook(payload)

@router.post("/webhooks/confluence")
async def confluence_webhook(request: Request):
    payload = await request.json()
    return ConfluenceConnector().ingest_webhook(payload)
