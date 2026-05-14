from typing import Dict, Any, Optional
from mock_simulation.scenarios.schema import UnifiedEvent
from mock_simulation.generators.base import GeneratorBase
from mock_simulation.timelines.engine import TimelineEngine

class ConfluenceGenerator(GeneratorBase):
    def generate_rca(self, timeline: TimelineEngine, org_id: str, title: str, content: str, related_incident_id: str) -> UnifiedEvent:
        page_id = f"CONF-{self.faker.random_int(min=100000, max=999999)}"
        event = UnifiedEvent(
            event_id=self.faker.uuid4(),
            source="Confluence",
            event_type="page_created",
            timestamp=timeline.get_current_time_iso(),
            organization_id=org_id,
            metadata={
                "page_id": page_id,
                "title": title,
                "content": content,
                "author": self.faker.email(),
                "labels": ["rca", "postmortem"],
                "related_incident": related_incident_id
            }
        )
        timeline.record_event(event)
        return event

    def generate_sop(self, timeline: TimelineEngine, org_id: str, title: str, content: str) -> UnifiedEvent:
        page_id = f"CONF-{self.faker.random_int(min=100000, max=999999)}"
        event = UnifiedEvent(
            event_id=self.faker.uuid4(),
            source="Confluence",
            event_type="page_created",
            timestamp=timeline.get_current_time_iso(),
            organization_id=org_id,
            metadata={
                "page_id": page_id,
                "title": title,
                "content": content,
                "author": self.faker.email(),
                "labels": ["sop", "runbook"]
            }
        )
        timeline.record_event(event)
        return event
