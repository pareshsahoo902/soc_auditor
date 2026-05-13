import json
import logging
from typing import List
from shared.models.database import GovernanceFinding, Event

logger = logging.getLogger(__name__)

class ReportGenerator:
    @staticmethod
    def generate_json_audit_packet(event: Event, findings: List[GovernanceFinding]) -> str:
        packet = {
            "incident_id": event.event_id,
            "timestamp": event.timestamp.isoformat(),
            "findings": [
                {
                    "rule": f.rule_name,
                    "severity": f.severity,
                    "finding": f.finding,
                    "soc2_mapping": f.evidence_json.get("soc2")
                } for f in findings
            ],
            "hygiene_score": event.metadata_json.get("hygiene_score", 100)
        }
        return json.dumps(packet, indent=2)

    @staticmethod
    def export_csv(findings: List[GovernanceFinding]) -> str:
        # Mock CSV export
        header = "Rule,Severity,Finding,SOC2\n"
        rows = [f"{f.rule_name},{f.severity},{f.finding},{f.evidence_json.get('soc2')}" for f in findings]
        return header + "\n".join(rows)
