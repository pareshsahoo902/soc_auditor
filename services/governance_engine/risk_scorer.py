import logging
from typing import List
from shared.models.database import GovernanceFinding

logger = logging.getLogger(__name__)

class RiskScorer:
    @staticmethod
    def calculate_incident_hygiene_score(findings: List[GovernanceFinding]) -> int:
        score = 100
        for f in findings:
            if f.severity == "critical":
                score -= 30
            elif f.severity == "high":
                score -= 15
            elif f.severity == "medium":
                score -= 5
            elif f.severity == "low":
                score -= 2

        return max(0, score)

    @staticmethod
    def calculate_organizational_risk(incident_scores: List[int]) -> dict:
        if not incident_scores:
            return {"posture": "unknown", "average_score": 0}

        avg = sum(incident_scores) / len(incident_scores)
        posture = "healthy"
        if avg < 50:
            posture = "critical_risk"
        elif avg < 75:
            posture = "at_risk"

        return {"posture": posture, "average_score": round(avg, 2)}
