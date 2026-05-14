from typing import Dict, Any, Optional
from mock_simulation.core.models.events import UnifiedEvent
from mock_simulation.generators.base import GeneratorBase
from mock_simulation.timelines.engine import TimelineEngine

class GitHubGenerator(GeneratorBase):
    def generate_pr_created(self, timeline: TimelineEngine, org_id: str, repo: str, title: str, author: str) -> UnifiedEvent:
        pr_id = self.faker.random_int(min=1, max=1000)
        event = UnifiedEvent(
            event_id=self.id_gen.generate_id(self.faker.seed, "event", self.faker.random_int(1, 1000000)),
            source="GitHub",
            event_type="pull_request_created",
            entity_type="PullRequest",
            timestamp=timeline.get_current_time_iso(),
            organization_id=org_id,
            metadata={
                "pr_id": pr_id,
                "repo": repo,
                "title": title,
                "author": author,
                "state": "open"
            }
        )
        timeline.record_event(event)
        return event

    def generate_pr_approved(self, timeline: TimelineEngine, org_id: str, repo: str, pr_id: int, reviewer: str) -> UnifiedEvent:
        event = UnifiedEvent(
            event_id=self.id_gen.generate_id(self.faker.seed, "event", self.faker.random_int(1, 1000000)),
            source="GitHub",
            event_type="pull_request_approved",
            entity_type="PullRequest",
            timestamp=timeline.get_current_time_iso(),
            organization_id=org_id,
            metadata={
                "pr_id": pr_id,
                "repo": repo,
                "reviewer": reviewer,
                "state": "approved"
            }
        )
        timeline.record_event(event)
        return event

    def generate_pr_merged(self, timeline: TimelineEngine, org_id: str, repo: str, pr_id: int, merged_by: str) -> UnifiedEvent:
        commit_sha = self.faker.sha1()
        event = UnifiedEvent(
            event_id=self.id_gen.generate_id(self.faker.seed, "event", self.faker.random_int(1, 1000000)),
            source="GitHub",
            event_type="pull_request_merged",
            entity_type="PullRequest",
            timestamp=timeline.get_current_time_iso(),
            organization_id=org_id,
            metadata={
                "pr_id": pr_id,
                "repo": repo,
                "merged_by": merged_by,
                "commit_sha": commit_sha,
                "state": "merged"
            }
        )
        timeline.record_event(event)
        return event
