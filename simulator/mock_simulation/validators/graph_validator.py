from typing import List, Dict, Any, Tuple
from mock_simulation.core.models.events import UnifiedEvent

class EvidenceGraphValidator:
    @staticmethod
    def validate(events: List[UnifiedEvent]) -> Dict[str, Any]:
        """
        Validates the evidence graph by ensuring no 'relationship_created' events point to missing entities.
        Returns a dictionary with validation results including orphans and broken links.
        """
        entities = set()
        relationships = []
        orphan_nodes = []
        broken_relationships = []

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
                relationships.append({
                    "source": event.metadata.get("source_entity_id"),
                    "target": event.metadata.get("target_entity_id"),
                    "type": event.metadata.get("relationship_type")
                })

        # Verify relationships
        for rel in relationships:
            source_id = rel["source"]
            target_id = rel["target"]

            source_exists = source_id in entities
            target_exists = target_id in entities

            if not source_exists and not target_exists:
                orphan_nodes.extend([source_id, target_id])
                broken_relationships.append(rel)
            elif not source_exists:
                orphan_nodes.append(source_id)
                broken_relationships.append(rel)
            elif not target_exists:
                orphan_nodes.append(target_id)
                broken_relationships.append(rel)

        return {
            "is_valid": len(orphan_nodes) == 0 and len(broken_relationships) == 0,
            "orphan_nodes": orphan_nodes,
            "broken_relationships": broken_relationships
        }
