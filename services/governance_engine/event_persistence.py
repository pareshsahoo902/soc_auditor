from shared.models.database import SessionLocal, Event
from shared.schemas.events import UnifiedEvent
import logging

logger = logging.getLogger(__name__)

class EventPersistence:
    @staticmethod
    def save_event(event: UnifiedEvent) -> bool:
        db = SessionLocal()
        try:
            # Check for duplicate
            existing = db.query(Event).filter(Event.event_id == event.event_id).first()
            if existing:
                logger.warning(f"Event {event.event_id} already exists.")
                return False

            db_event = Event(
                event_id=event.event_id,
                source=event.source,
                event_type=event.event_type,
                timestamp=event.timestamp,
                metadata_json=event.metadata
            )
            db.add(db_event)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save event {event.event_id}: {e}")
            return False
        finally:
            db.close()
