import logging
from shared.models.database import SessionLocal, Event, EvidenceLink

logger = logging.getLogger(__name__)

class EvidenceGraphBuilder:
    @staticmethod
    def link_events(source_id: str, target_id: str, relationship_type: str):
        db = SessionLocal()
        try:
            source = db.query(Event).filter(Event.event_id == source_id).first()
            target = db.query(Event).filter(Event.event_id == target_id).first()

            if not source or not target:
                logger.warning("Could not create evidence link: events not found")
                return False

            link = EvidenceLink(
                source_event_id=source.id,
                target_event_id=target.id,
                relationship_type=relationship_type
            )
            db.add(link)
            db.commit()
            return True
        finally:
            db.close()

    @staticmethod
    def detect_orphan_events():
        # Logic to find events with no relationships (e.g., untracked PRs, incidents without RCAs)
        pass
