import logging
from apps.worker.tasks import process_ingestion
from datetime import datetime

logger = logging.getLogger(__name__)

class GitHubConnector:
    def ingest_webhook(self, payload: dict):
        event_id = payload.get("pull_request", {}).get("id", f"PR-{datetime.utcnow().timestamp()}")
        normalized = {
            "event_id": str(event_id),
            "source": "github",
            "event_type": "pr_merged",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": payload
        }
        process_ingestion.delay(normalized)
        return normalized
