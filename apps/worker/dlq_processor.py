import logging

logger = logging.getLogger(__name__)

class DLQProcessor:
    @staticmethod
    def process_failed_event(event_data: dict, error: str):
        logger.error(f"Moving event {event_data.get('event_id')} to DLQ. Error: {error}")
        # In a real system, persist this to a specific DLQ table or Redis stream
        pass
