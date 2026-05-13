from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class UnifiedEvent(BaseModel):
    event_id: str
    source: str = Field(..., description="E.g., jira, github, zendesk, confluence")
    event_type: str = Field(..., description="E.g., incident_created, pr_merged")
    timestamp: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)
