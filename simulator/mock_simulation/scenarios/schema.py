from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class UnifiedEvent(BaseModel):
    event_id: str = Field(..., description="Unique identifier for the event")
    source: str = Field(..., description="Source system (e.g., Jira, GitHub, Zendesk)")
    event_type: str = Field(..., description="Type of event (e.g., incident_created, pr_merged)")
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp")
    organization_id: str = Field(..., description="ID of the organization")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Event-specific metadata")
