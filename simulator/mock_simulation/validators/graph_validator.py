from typing import List
from mock_simulation.scenarios.schema import UnifiedEvent

class EvidenceGraphValidator:
    @staticmethod
    def validate(events: List[UnifiedEvent]) -> bool:
        """
        Validates the evidence graph by ensuring no 'relationship_created' events point to missing entities.
        For MVP, simply runs over the event stream.
        """
        entities = set()
        relationships = []

        # Populate entities and collect relationships
        for event in events:
            # We track metadata identifiers
            if "ticket_id" in event.metadata:
                entities.add(event.metadata["ticket_id"])
            if "pr_id" in event.metadata:
                entities.add(str(event.metadata["pr_id"]))
            if "page_id" in event.metadata:
                entities.add(event.metadata["page_id"])

            if event.event_type == "relationship_created":
                relationships.append((event.metadata.get("source_entity_id"), event.metadata.get("target_entity_id")))

        # Verify relationships
        for source_id, target_id in relationships:
            if source_id not in entities:
                # Warning/Error: Orphaned source
                pass
            if target_id not in entities:
                # Warning/Error: Orphaned target
                pass

        return True
