from typing import List, Dict, Any
from mock_simulation.scenarios.base import BaseScenario
from mock_simulation.scenarios.schema import UnifiedEvent
from mock_simulation.scenarios.registry import ScenarioRegistry
from mock_simulation.timelines.engine import TimelineEngine
from mock_simulation.generators.github import GitHubGenerator

@ScenarioRegistry.register("missing_approval")
class MissingApprovalScenario(BaseScenario):
    def generate_events(self, timeline: TimelineEngine, org_id: str) -> List[UnifiedEvent]:
        github = GitHubGenerator(self.faker)

        # 00:00 PR Created
        author = self.faker.email()
        pr_event = github.generate_pr_created(timeline, org_id, "core-api", "Emergency fix without review", author)
        pr_id = pr_event.metadata["pr_id"]

        # 00:02 PR Merged without approval (Bypass)
        timeline.advance_time(minutes=2)
        github.generate_pr_merged(timeline, org_id, "core-api", pr_id, author)

        return timeline.get_events()

    def expected_findings(self) -> List[Dict[str, Any]]:
        return [
            {"finding_type": "soc2_cc8_violation", "severity": "critical", "description": "PR merged without required approvals"}
        ]

    def expected_graph(self) -> List[Dict[str, Any]]:
        return []

    def expected_slas(self) -> List[Dict[str, Any]]:
        return []
