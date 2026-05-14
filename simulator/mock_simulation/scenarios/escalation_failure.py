from typing import List, Dict, Any
from mock_simulation.scenarios.base import BaseScenario
from mock_simulation.core.models.events import UnifiedEvent
from mock_simulation.scenarios.registry import ScenarioRegistry
from mock_simulation.timelines.engine import TimelineEngine
from mock_simulation.generators.jira import JiraGenerator
from mock_simulation.core.models.governance import BenchmarkType, FindingCategory, GovernanceSeverity

@ScenarioRegistry.register("escalation_failure")
class EscalationFailureScenario(BaseScenario):
    name = "Escalation Missed on SEV-1"
    description = "SEV-1 Incident unacknowledged without escalation."
    scenario_version = "1.0.0"
    benchmark_type = BenchmarkType.GOVERNANCE_FAILURE
    tags = ["jira", "incident", "escalation"]

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
            {
                "category": FindingCategory.ESCALATION_FAILURE.value,
                "severity": GovernanceSeverity.HIGH.value,
                "description": "SEV-1 incident unacknowledged without escalation."
            }
        ]

    def expected_slas(self) -> List[Dict[str, Any]]:
        return [{"metric": "time_to_acknowledge", "status": "breached"}]
