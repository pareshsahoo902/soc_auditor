import yaml
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class RuleEngine:
    def __init__(self, rules_path: str = "shared/configs/governance_rules.yaml"):
        with open(rules_path, "r") as f:
            self.config = yaml.safe_load(f)
            self.rules = self.config.get("rules", [])

    def evaluate(self, event: Dict) -> List[Dict]:
        findings = []
        event_type = event.get("event_type")

        for rule in self.rules:
            if rule["condition"].get("event_type") == event_type:
                logger.info(f"Evaluating rule {rule['id']} for event {event.get('event_id')}")

                # Mock evaluation logic for deterministic checks
                if rule["type"] == "rca_completeness":
                    findings.append(self._mock_rca_check(rule, event))
                elif rule["type"] == "change_management":
                    findings.append(self._mock_change_check(rule, event))
                elif rule["type"] == "sla_validation":
                    findings.append(self._mock_sla_check(rule, event))

        return [f for f in findings if f is not None]

    def _mock_rca_check(self, rule, event):
        metadata = event.get("metadata", {})
        if not metadata.get("root_cause"):
            return {
                "rule_id": rule["id"],
                "finding": "Missing root cause in RCA",
                "severity": "high",
                "soc2_mapping": rule["soc2_mapping"]
            }
        return None

    def _mock_change_check(self, rule, event):
        metadata = event.get("metadata", {})
        if not metadata.get("approvals"):
            return {
                "rule_id": rule["id"],
                "finding": "PR merged without approvals",
                "severity": "critical",
                "soc2_mapping": rule["soc2_mapping"]
            }
        return None

    def _mock_sla_check(self, rule, event):
        return None # Mock pass
