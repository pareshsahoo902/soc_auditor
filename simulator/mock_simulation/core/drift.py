from typing import List, Dict, Any

class GovernanceDriftEngine:
    @staticmethod
    def detect_drift(expected_workflow: List[str], observed_workflow: List[str]) -> Dict[str, Any]:
        """
        Detects drift between expected workflow sequence and observed sequence.
        """
        drift_points = []
        is_drifted = False

        expected_idx = 0
        observed_idx = 0

        while expected_idx < len(expected_workflow) and observed_idx < len(observed_workflow):
            if expected_workflow[expected_idx] == observed_workflow[observed_idx]:
                expected_idx += 1
                observed_idx += 1
            else:
                is_drifted = True
                drift_points.append({
                    "expected": expected_workflow[expected_idx],
                    "observed": observed_workflow[observed_idx]
                })
                # Simple recovery: advance observed to try and catch up
                observed_idx += 1

        # Any remaining expected steps were skipped
        while expected_idx < len(expected_workflow):
            is_drifted = True
            drift_points.append({
                "expected": expected_workflow[expected_idx],
                "observed": None
            })
            expected_idx += 1

        return {
            "has_drift": is_drifted,
            "drift_points": drift_points
        }

    @staticmethod
    def calculate_confidence(evidence_count: int, has_broken_links: bool) -> float:
        """
        Deterministic confidence heuristic.
        """
        confidence = 1.0
        if has_broken_links:
            confidence -= 0.3

        if evidence_count == 0:
            confidence -= 0.5
        elif evidence_count == 1:
            confidence -= 0.1

        return max(0.0, min(1.0, confidence))
