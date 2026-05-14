from typing import List, Dict, Any
from mock_simulation.scenarios.base import BaseScenario
from mock_simulation.core.models.events import UnifiedEvent
from mock_simulation.scenarios.registry import ScenarioRegistry
from mock_simulation.timelines.engine import TimelineEngine
from mock_simulation.generators.jira import JiraGenerator
from mock_simulation.generators.github import GitHubGenerator
from mock_simulation.generators.confluence import ConfluenceGenerator
from mock_simulation.generators.relationship import RelationshipGenerator
from mock_simulation.core.models.governance import BenchmarkType

@ScenarioRegistry.register("sev1_outage")
class Sev1Scenario(BaseScenario):
    name = "SEV-1 Outage Happy Path"
    description = "A standard SEV-1 incident handled perfectly within SLAs."
    scenario_version = "1.0.0"
    benchmark_type = BenchmarkType.HAPPY_PATH
    tags = ["sev1", "incident", "happy_path"]

    def generate_events(self, timeline: TimelineEngine, org_id: str) -> List[UnifiedEvent]:
        jira = JiraGenerator(self.faker)
        github = GitHubGenerator(self.faker)
        confluence = ConfluenceGenerator(self.faker)
        rel = RelationshipGenerator(self.faker)

        # 00:00 Incident Created
        incident_event = jira.generate_ticket(timeline, org_id, "SEV-1", "Database Outage in Production")
        ticket_id = incident_event.metadata["ticket_id"]

        # 00:05 Acknowledged
        timeline.advance_time(minutes=5)
        jira.generate_status_transition(timeline, org_id, ticket_id, "In Progress")

        # 00:30 Fix PR Created
        timeline.advance_time(minutes=25)
        pr_event = github.generate_pr_created(timeline, org_id, "backend-service", "Fix DB connection pool", self.faker.email())
        pr_id = pr_event.metadata["pr_id"]

        # 00:35 Fix PR Approved
        timeline.advance_time(minutes=5)
        github.generate_pr_approved(timeline, org_id, "backend-service", pr_id, self.faker.email())

        # 00:40 Fix PR Merged
        timeline.advance_time(minutes=5)
        github.generate_pr_merged(timeline, org_id, "backend-service", pr_id, self.faker.email())

        # 00:45 Relationship mapped
        timeline.advance_time(minutes=5)
        rel.generate_mapping(timeline, org_id, ticket_id, str(pr_id), "incident_to_pr")

        # 01:00 Incident Resolved
        timeline.advance_time(minutes=15)
        jira.generate_status_transition(timeline, org_id, ticket_id, "Resolved")

        # 02:00 RCA Created
        timeline.advance_time(hours=1)
        rca_event = confluence.generate_rca(timeline, org_id, f"RCA: {ticket_id} Database Outage", "We ran out of connections. Increased pool size.", ticket_id)
        rca_id = rca_event.metadata["page_id"]

        # 02:05 Relationship mapped
        timeline.advance_time(minutes=5)
        rel.generate_mapping(timeline, org_id, ticket_id, rca_id, "incident_to_rca")

        return timeline.get_events()

    def expected_findings(self) -> List[Dict[str, Any]]:
        return []

    def expected_graph(self) -> List[Dict[str, Any]]:
        return [
            {"source_type": "jira_issue", "target_type": "github_pr", "relationship": "incident_to_pr"},
            {"source_type": "jira_issue", "target_type": "confluence_page", "relationship": "incident_to_rca"}
        ]

    def expected_slas(self) -> List[Dict[str, Any]]:
        return [{"metric": "resolution_time", "status": "met"}]
