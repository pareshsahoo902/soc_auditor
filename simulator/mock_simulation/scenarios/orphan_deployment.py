from typing import List, Dict, Any
from mock_simulation.scenarios.base import BaseScenario
from mock_simulation.core.models.events import UnifiedEvent
from mock_simulation.scenarios.registry import ScenarioRegistry
from mock_simulation.timelines.engine import TimelineEngine
from mock_simulation.generators.relationship import RelationshipGenerator
from mock_simulation.core.models.governance import BenchmarkType, FindingCategory, GovernanceSeverity

@ScenarioRegistry.register("orphan_deployment")
class OrphanDeploymentScenario(BaseScenario):
    name = "Orphan Deployment"
    description = "A deployment occurs but has no link back to a Jira Ticket or PR."
    scenario_version = "1.0.0"
    benchmark_type = BenchmarkType.GOVERNANCE_FAILURE
    tags = ["deployment", "evidence_graph"]

    def generate_events(self, timeline: TimelineEngine, org_id: str) -> List[UnifiedEvent]:
        rel = RelationshipGenerator(self.faker)

        # 00:00 A deployment happens, recorded by some system.
        # However, there is no corresponding PR or Jira Ticket event.
        deployment_id = f"deploy_{self.faker.sha1()[:8]}"

        # We record a relationship from this deployment pointing to a non-existent ticket to trigger graph invalidity
        event = rel.generate_mapping(timeline, org_id, deployment_id, "TICKET-UNKNOWN", "deployment_to_ticket")

        return timeline.get_events()

    def expected_findings(self) -> List[Dict[str, Any]]:
        return [
            {
                "category": FindingCategory.EVIDENCE_GAP.value,
                "severity": GovernanceSeverity.HIGH.value,
                "description": "Deployment is missing traceability to an approved change or incident."
            }
        ]

    def expected_graph(self) -> List[Dict[str, Any]]:
        # Expect an invalid graph structure due to missing ticket
        return []
