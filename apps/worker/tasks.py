from apps.worker.celery_app import celery_app
from services.governance_engine.event_validator import EventValidator
from services.governance_engine.event_persistence import EventPersistence
from apps.worker.dlq_processor import DLQProcessor
from services.rule_engine.evaluator import RuleEngine
from services.ai_router.router import AIRouter
from services.governance_engine.risk_scorer import RiskScorer
from shared.models.database import SessionLocal, GovernanceFinding, Event
import logging

logger = logging.getLogger(__name__)
rule_engine = RuleEngine()
ai_router = AIRouter()
risk_scorer = RiskScorer()

@celery_app.task(bind=True, max_retries=3)
def process_ingestion(self, event_data: dict):
    logger.info(f"Processing ingestion for event: {event_data.get('event_id')}")
    validated_event = EventValidator.validate(event_data)
    if not validated_event:
        DLQProcessor.process_failed_event(event_data, "Validation failed")
        return {"status": "failed"}
    saved = EventPersistence.save_event(validated_event)
    if saved:
        process_extraction.delay(validated_event.event_id)
    return {"status": "ingested"}

@celery_app.task
def process_extraction(event_id: str):
    logger.info(f"Processing extraction for event: {event_id}")
    process_governance.delay(event_id)
    return {"status": "extracted"}

@celery_app.task
def process_governance(event_id: str):
    logger.info(f"Processing governance for event: {event_id}")

    db = SessionLocal()
    try:
        event = db.query(Event).filter(Event.event_id == event_id).first()
        if not event:
            return {"status": "error"}

        event_dict = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "metadata": event.metadata_json
        }

        findings = rule_engine.evaluate(event_dict)
        finding_records = []
        for f in findings:
            finding_record = GovernanceFinding(
                event_id=event.id,
                rule_name=f["rule_id"],
                severity=f["severity"],
                finding=f["finding"],
                evidence_json={"soc2": f["soc2_mapping"]}
            )
            db.add(finding_record)
            finding_records.append(finding_record)

        db.commit()

        # Calculate Risk Score
        score = risk_scorer.calculate_incident_hygiene_score(finding_records)
        new_metadata = dict(event.metadata_json) if event.metadata_json else {}
        new_metadata["hygiene_score"] = score
        event.metadata_json = new_metadata
        db.commit()

        process_reporting.delay(event_id)
        return {"status": "evaluated", "score": score}
    finally:
        db.close()

@celery_app.task
def process_reporting(event_id: str):
    logger.info(f"Processing reporting for event: {event_id}")
    return {"status": "reported"}
