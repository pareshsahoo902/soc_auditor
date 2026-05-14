from typing import List, Dict, Any
from mock_simulation.scenarios.base import BaseScenario
from mock_simulation.scenarios.schema import UnifiedEvent
from mock_simulation.scenarios.registry import ScenarioRegistry
from mock_simulation.timelines.engine import TimelineEngine
from mock_simulation.generators.jira import JiraGenerator

@ScenarioRegistry.register("escalation_failure")
class EscalationFailureScenario(BaseScenario):
    def generate_events(self, timeline: TimelineEngine, org_id: str) -> List[UnifiedEvent]:
        jira = JiraGenerator(self.faker)

        # 00:00 SEV-1 Incident Created
        incident_event = jira.generate_ticket(timeline, org_id, "SEV-1", "Payment Gateway Down")
        ticket_id = incident_event.metadata["ticket_id"]

        # 00:05 Ticket left unassigned, no escalation generated for hours
        timeline.advance_time(hours=2)

        # 02:00 Ticket finally assigned (too late for SEV-1 SLA)
        jira.generate_status_transition(timeline, org_id, ticket_id, "In Progress")

        return timeline.get_events()

    def expected_findings(self) -> List[Dict[str, Any]]:
        return [
            {"finding_type": "escalation_missed", "severity": "high", "description": "SEV-1 incident unacknowledged without escalation."}
        ]

    def expected_graph(self) -> List[Dict[str, Any]]:
        return []

    def expected_slas(self) -> List[Dict[str, Any]]:
        return [{"metric": "time_to_acknowledge", "status": "breached"}]
