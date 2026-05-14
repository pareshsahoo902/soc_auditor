from typing import Dict, Any, Optional, List
from mock_simulation.scenarios.schema import UnifiedEvent
from mock_simulation.generators.base import GeneratorBase
from mock_simulation.timelines.engine import TimelineEngine

class RelationshipGenerator(GeneratorBase):
    def generate_mapping(self, timeline: TimelineEngine, org_id: str, source_id: str, target_id: str, relationship_type: str) -> UnifiedEvent:
        """
        Creates a generic relationship event, often emitted by a webhook aggregating multiple tools
        (like a unified governance platform webhook).
        """
        event = UnifiedEvent(
            event_id=self.faker.uuid4(),
            source="System",
            event_type="relationship_created",
            timestamp=timeline.get_current_time_iso(),
            organization_id=org_id,
            metadata={
                "source_entity_id": source_id,
                "target_entity_id": target_id,
                "relationship_type": relationship_type # e.g., "incident_to_pr", "incident_to_rca"
            }
        )
        timeline.record_event(event)
        return event
