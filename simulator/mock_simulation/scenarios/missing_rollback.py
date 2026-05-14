from typing import List, Dict, Any
from mock_simulation.scenarios.base import BaseScenario
from mock_simulation.core.models.events import UnifiedEvent
from mock_simulation.scenarios.registry import ScenarioRegistry
from mock_simulation.timelines.engine import TimelineEngine
from mock_simulation.generators.github import GitHubGenerator
from mock_simulation.core.models.governance import BenchmarkType, FindingCategory, GovernanceSeverity

@ScenarioRegistry.register("missing_rollback")
class MissingRollbackScenario(BaseScenario):
    name = "Missing Rollback Plan"
    description = "PR merged without a rollback plan in its description."
    scenario_version = "1.0.0"
    benchmark_type = BenchmarkType.GOVERNANCE_FAILURE
    tags = ["github", "pr", "change_management"]

    def generate_events(self, timeline: TimelineEngine, org_id: str) -> List[UnifiedEvent]:
        github = GitHubGenerator(self.faker)

        # 00:00 PR Created without rollback plan
        author = self.faker.email()
        desc = "Implemented new feature X. LGTM."
        pr_event = github.generate_pr_created(timeline, org_id, "frontend-app", desc, author)
        pr_id = pr_event.metadata["pr_id"]

        # 00:05 PR Approved
        timeline.advance_time(minutes=5)
        github.generate_pr_approved(timeline, org_id, "frontend-app", pr_id, self.faker.email())

        # 00:10 PR Merged
        timeline.advance_time(minutes=5)
        github.generate_pr_merged(timeline, org_id, "frontend-app", pr_id, author)

        return timeline.get_events()

    def expected_findings(self) -> List[Dict[str, Any]]:
        return [
            {
                "category": FindingCategory.CHANGE_GOVERNANCE.value,
                "severity": GovernanceSeverity.MEDIUM.value,
                "description": "PR merged without documented rollback plan."
            }
        ]
