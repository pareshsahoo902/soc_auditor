from typing import List, Dict, Any
from mock_simulation.scenarios.base import BaseScenario
from mock_simulation.core.models.events import UnifiedEvent
from mock_simulation.scenarios.registry import ScenarioRegistry
from mock_simulation.timelines.engine import TimelineEngine
from mock_simulation.generators.jira import JiraGenerator
from mock_simulation.generators.confluence import ConfluenceGenerator
from mock_simulation.core.models.governance import BenchmarkType, FindingCategory, GovernanceSeverity

@ScenarioRegistry.register("weak_rca")
class WeakRCAScenario(BaseScenario):
    name = "Weak RCA Detected"
    description = "Incident is closed but RCA lacks root cause and action items."
    scenario_version = "1.0.0"
    benchmark_type = BenchmarkType.GOVERNANCE_FAILURE
    tags = ["confluence", "jira", "rca", "incident"]

    def generate_events(self, timeline: TimelineEngine, org_id: str) -> List[UnifiedEvent]:
        jira = JiraGenerator(self.faker)
        confluence = ConfluenceGenerator(self.faker)

        # 00:00 Incident Created
        incident_event = jira.generate_ticket(timeline, org_id, "SEV-2", "Intermittent 502s")
        ticket_id = incident_event.metadata["ticket_id"]

        # 01:00 Incident Resolved
        timeline.advance_time(hours=1)
        jira.generate_status_transition(timeline, org_id, ticket_id, "Resolved")

        # 02:00 Weak RCA Created
        timeline.advance_time(hours=1)
        weak_content = "There were some errors. We restarted the pods and it worked. No further action needed."
        confluence.generate_rca(timeline, org_id, f"RCA: {ticket_id}", weak_content, ticket_id)

        return timeline.get_events()

    def expected_findings(self) -> List[Dict[str, Any]]:
        return [
            {
                "category": FindingCategory.RCA_QUALITY.value,
                "severity": GovernanceSeverity.MEDIUM.value,
                "description": "RCA lacks clear root cause and remediation steps."
            }
        ]
