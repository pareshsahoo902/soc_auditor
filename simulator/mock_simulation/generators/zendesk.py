from typing import Dict, Any, Optional
from mock_simulation.scenarios.schema import UnifiedEvent
from mock_simulation.generators.base import GeneratorBase
from mock_simulation.timelines.engine import TimelineEngine

class ZendeskGenerator(GeneratorBase):
    def generate_customer_ticket(self, timeline: TimelineEngine, org_id: str, subject: str, description: str) -> UnifiedEvent:
        ticket_id = f"ZD-{self.faker.random_int(min=10000, max=99999)}"
        event = UnifiedEvent(
            event_id=self.faker.uuid4(),
            source="Zendesk",
            event_type="ticket_created",
            timestamp=timeline.get_current_time_iso(),
            organization_id=org_id,
            metadata={
                "ticket_id": ticket_id,
                "subject": subject,
                "description": description,
                "requester": self.faker.email()
            }
        )
        timeline.record_event(event)
        return event

    def generate_sla_breach(self, timeline: TimelineEngine, org_id: str, ticket_id: str, breach_type: str) -> UnifiedEvent:
        event = UnifiedEvent(
            event_id=self.faker.uuid4(),
            source="Zendesk",
            event_type="sla_breach",
            timestamp=timeline.get_current_time_iso(),
            organization_id=org_id,
            metadata={
                "ticket_id": ticket_id,
                "breach_type": breach_type, # e.g., "first_reply_time", "resolution_time"
            }
        )
        timeline.record_event(event)
        return event
