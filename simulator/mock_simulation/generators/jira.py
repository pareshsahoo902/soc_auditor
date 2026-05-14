from typing import Dict, Any, Optional
from mock_simulation.core.models.events import UnifiedEvent
from mock_simulation.generators.base import GeneratorBase
from mock_simulation.timelines.engine import TimelineEngine

class JiraGenerator(GeneratorBase):
    def generate_ticket(self, timeline: TimelineEngine, org_id: str, severity: str, summary: str, status: str = "Open") -> UnifiedEvent:
        ticket_id = f"ENG-{self.faker.random_int(min=1000, max=9999)}"
        event = UnifiedEvent(
            event_id=self.id_gen.generate_id(self.faker.seed, "event", self.faker.random_int(1, 1000000)),
            source="Jira",
            event_type="issue_created",
            entity_type="Ticket",
            timestamp=timeline.get_current_time_iso(),
            organization_id=org_id,
            metadata={
                "ticket_id": ticket_id,
                "severity": severity,
                "summary": summary,
                "status": status,
                "reporter": self.faker.email(),
                "assignee": None
            }
        )
        timeline.record_event(event)
        return event

    def generate_status_transition(self, timeline: TimelineEngine, org_id: str, ticket_id: str, new_status: str) -> UnifiedEvent:
        event = UnifiedEvent(
            event_id=self.id_gen.generate_id(self.faker.seed, "event", self.faker.random_int(1, 1000000)),
            source="Jira",
            event_type="issue_updated",
            entity_type="Ticket",
            timestamp=timeline.get_current_time_iso(),
            organization_id=org_id,
            metadata={
                "ticket_id": ticket_id,
                "status": new_status,
                "update_type": "status_change"
            }
        )
        timeline.record_event(event)
        return event

    def generate_comment(self, timeline: TimelineEngine, org_id: str, ticket_id: str, comment: str) -> UnifiedEvent:
        event = UnifiedEvent(
            event_id=self.id_gen.generate_id(self.faker.seed, "event", self.faker.random_int(1, 1000000)),
            source="Jira",
            event_type="issue_commented",
            entity_type="Ticket",
            timestamp=timeline.get_current_time_iso(),
            organization_id=org_id,
            metadata={
                "ticket_id": ticket_id,
                "comment": comment,
                "author": self.faker.email()
            }
        )
        timeline.record_event(event)
        return event

    def generate_escalation(self, timeline: TimelineEngine, org_id: str, ticket_id: str, escalated_to: str) -> UnifiedEvent:
        event = UnifiedEvent(
            event_id=self.id_gen.generate_id(self.faker.seed, "event", self.faker.random_int(1, 1000000)),
            source="Jira",
            event_type="issue_escalated",
            entity_type="Escalation",
            timestamp=timeline.get_current_time_iso(),
            organization_id=org_id,
            metadata={
                "ticket_id": ticket_id,
                "escalated_to": escalated_to,
            }
        )
        timeline.record_event(event)
        return event
