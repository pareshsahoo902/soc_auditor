from typing import List, Dict, Any
from mock_simulation.core.models.governance import FindingCategory

class ScoringWeights:
    WEIGHTS = {
        FindingCategory.CHANGE_GOVERNANCE: 30.0,
        FindingCategory.RCA_QUALITY: 20.0,
        FindingCategory.SLA_VIOLATION: 15.0,
        FindingCategory.EVIDENCE_GAP: 25.0,
        FindingCategory.ESCALATION_FAILURE: 10.0,
        FindingCategory.PROCESS_DRIFT: 10.0,
        FindingCategory.AUDIT_READINESS: 20.0
    }

class GovernanceScoringEngine:
    @staticmethod
    def calculate_scores(findings: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculates deterministic weighted scores based on findings.
        Returns a dict of score categories to their computed values (0-100).
        """
        # Base scores start at 100
        scores = {
            "Incident Hygiene Score": 100.0,
            "RCA Quality Score": 100.0,
            "Change Governance Score": 100.0,
            "Audit Readiness Score": 100.0
        }

        for finding in findings:
            cat = finding.get("category")
            weight = ScoringWeights.WEIGHTS.get(cat, 0.0)

            if cat == FindingCategory.CHANGE_GOVERNANCE.value:
                scores["Change Governance Score"] = max(0.0, scores["Change Governance Score"] - weight)
                scores["Audit Readiness Score"] = max(0.0, scores["Audit Readiness Score"] - (weight * 0.5))

            elif cat == FindingCategory.RCA_QUALITY.value:
                scores["RCA Quality Score"] = max(0.0, scores["RCA Quality Score"] - weight)
                scores["Incident Hygiene Score"] = max(0.0, scores["Incident Hygiene Score"] - (weight * 0.5))

            elif cat in [FindingCategory.SLA_VIOLATION.value, FindingCategory.ESCALATION_FAILURE.value]:
                scores["Incident Hygiene Score"] = max(0.0, scores["Incident Hygiene Score"] - weight)

            elif cat in [FindingCategory.EVIDENCE_GAP.value, FindingCategory.PROCESS_DRIFT.value]:
                scores["Audit Readiness Score"] = max(0.0, scores["Audit Readiness Score"] - weight)

        return scores
