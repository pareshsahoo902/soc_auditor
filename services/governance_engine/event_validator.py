from shared.schemas.events import UnifiedEvent
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

class EventValidator:
    @staticmethod
    def validate(raw_event: dict) -> UnifiedEvent | None:
        try:
            return UnifiedEvent(**raw_event)
        except ValidationError as e:
            logger.error(f"Event validation failed: {e}")
            return None
