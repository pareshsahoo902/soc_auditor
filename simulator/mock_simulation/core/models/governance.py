from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class EntityType(str, Enum):
    INCIDENT = "Incident"
    TICKET = "Ticket"
    PULL_REQUEST = "PullRequest"
    DEPLOYMENT = "Deployment"
    APPROVAL = "Approval"
    RCA = "RCA"
    SLA_EVENT = "SLAEvent"
    ESCALATION = "Escalation"
    POSTMORTEM = "Postmortem"
    GOVERNANCE_FINDING = "GovernanceFinding"

class GovernanceSeverity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class FindingCategory(str, Enum):
    SLA_VIOLATION = "SLA_VIOLATION"
    CHANGE_GOVERNANCE = "CHANGE_GOVERNANCE"
    RCA_QUALITY = "RCA_QUALITY"
    EVIDENCE_GAP = "EVIDENCE_GAP"
    ESCALATION_FAILURE = "ESCALATION_FAILURE"
    PROCESS_DRIFT = "PROCESS_DRIFT"
    AUDIT_READINESS = "AUDIT_READINESS"

class BenchmarkType(str, Enum):
    HAPPY_PATH = "happy_path"
    GOVERNANCE_FAILURE = "governance_failure"
    CHAOS = "chaos"
    SCALE = "scale"
    EDGE_CASE = "edge_case"

class GovernanceControl(BaseModel):
    control_id: str = Field(..., description="E.g., SOC2 CC7")
    framework: str = Field(..., description="E.g., SOC2")
    title: str = Field(..., description="Control title or description")

class GovernanceExplanation(BaseModel):
    why: str = Field(..., description="Detailed explanation of the finding")
    impacted_controls: List[GovernanceControl] = Field(default_factory=list, description="List of controls impacted by the finding")
    evidence_references: List[str] = Field(default_factory=list, description="Entity IDs that provide evidence")
    operational_impact: str = Field(..., description="Description of the operational impact")

class GovernanceScore(BaseModel):
    score_type: str = Field(..., description="E.g., Incident Hygiene Score")
    score: float = Field(..., description="Numeric score")
    weight: float = Field(..., description="Weight of the score component")
    details: Dict[str, Any] = Field(default_factory=dict, description="Metadata explaining the score computation")

class GovernanceFinding(BaseModel):
    finding_id: str = Field(..., description="Deterministically generated ID")
    category: FindingCategory
    severity: GovernanceSeverity
    description: str = Field(..., description="Short finding description")
    explanation: GovernanceExplanation
    confidence: float = Field(..., description="Deterministic confidence score based on evidence links (e.g., 0.0 to 1.0)")
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict)
