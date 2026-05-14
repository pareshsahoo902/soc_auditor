from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from shared.models.database import SessionLocal, Event, GovernanceFinding
from services.reporting_engine.generator import ReportGenerator

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/findings")
def list_findings(db: Session = Depends(get_db)):
    findings = db.query(GovernanceFinding).limit(100).all()
    return findings

@router.get("/reports/audit/{event_id}")
def generate_audit_report(event_id: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    findings = db.query(GovernanceFinding).filter(GovernanceFinding.event_id == event.id).all()
    packet = ReportGenerator.generate_json_audit_packet(event, findings)
    return {"report": packet}
