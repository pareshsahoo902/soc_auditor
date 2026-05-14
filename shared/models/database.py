from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from shared.configs.settings import settings
import datetime

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"))
    name = Column(String)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True)
    source = Column(String)
    event_type = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    metadata_json = Column(JSON)

class GovernanceFinding(Base):
    __tablename__ = "governance_findings"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    rule_name = Column(String)
    severity = Column(String)
    finding = Column(String)
    evidence_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class EvidenceLink(Base):
    __tablename__ = "evidence_links"
    id = Column(Integer, primary_key=True, index=True)
    source_event_id = Column(Integer, ForeignKey("events.id"))
    target_event_id = Column(Integer, ForeignKey("events.id"))
    relationship_type = Column(String) # e.g., "resolves", "implements", "documents"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
