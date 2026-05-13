import logging
from apps.worker.tasks import process_ingestion
from datetime import datetime

logger = logging.getLogger(__name__)

class ZendeskConnector:
    def ingest_webhook(self, payload: dict):
        event_id = payload.get("ticket", {}).get("id", f"ZD-{datetime.utcnow().timestamp()}")
        normalized = {
            "event_id": str(event_id),
            "source": "zendesk",
            "event_type": "ticket_escalated",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": payload
        }
        process_ingestion.delay(normalized)
        return normalized
