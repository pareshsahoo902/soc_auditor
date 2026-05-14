import logging
from apps.worker.tasks import process_ingestion
from datetime import datetime

logger = logging.getLogger(__name__)

class ConfluenceConnector:
    def ingest_webhook(self, payload: dict):
        event_id = payload.get("page", {}).get("id", f"CONF-{datetime.utcnow().timestamp()}")
        normalized = {
            "event_id": str(event_id),
            "source": "confluence",
            "event_type": "rca_published",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": payload
        }
        process_ingestion.delay(normalized)
        return normalized
