import logging
from apps.worker.tasks import process_ingestion
from datetime import datetime

logger = logging.getLogger(__name__)

class JiraConnector:
    def ingest_webhook(self, payload: dict):
        # Mock transformation
        event_id = payload.get("issue", {}).get("key", f"JIRA-{datetime.utcnow().timestamp()}")
        normalized = {
            "event_id": event_id,
            "source": "jira",
            "event_type": "incident_updated",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": payload
        }
        process_ingestion.delay(normalized)
        return normalized
