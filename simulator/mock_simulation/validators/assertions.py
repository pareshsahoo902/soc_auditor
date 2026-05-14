from typing import List, Dict, Any

class GovernanceAssertionEngine:
    @staticmethod
    def assert_finding_exists(expected_findings: List[Dict[str, Any]], actual_findings: List[Dict[str, Any]]) -> bool:
        """
        Validates that expected findings are present in the actual findings.
        """
        if not expected_findings:
            return True # Nothing to assert

        # Simplistic check for MVP
        for expected in expected_findings:
            found = False
            for actual in actual_findings:
                if expected["finding_type"] == actual.get("finding_type"):
                    found = True
                    break
            if not found:
                raise AssertionError(f"Expected finding '{expected['finding_type']}' not found in actual findings.")
        return True

    @staticmethod
    def assert_graph_integrity(expected_graph: List[Dict[str, Any]], actual_graph: List[Dict[str, Any]]) -> bool:
        """
        Validates the expected graph relationships match reality.
        """
        if not expected_graph:
            return True

        # Simplistic check for MVP
        for expected in expected_graph:
            found = False
            for actual in actual_graph:
                if (expected.get("source_type") == actual.get("source_type") and
                    expected.get("target_type") == actual.get("target_type") and
                    expected.get("relationship") == actual.get("relationship")):
                    found = True
                    break
            if not found:
                raise AssertionError(f"Expected graph relationship '{expected}' not found.")
        return True

    @staticmethod
    def assert_sla_violation(expected_slas: List[Dict[str, Any]], actual_slas: List[Dict[str, Any]]) -> bool:
        """
        Validates SLA expectations.
        """
        if not expected_slas:
            return True

        for expected in expected_slas:
            found = False
            for actual in actual_slas:
                if expected["metric"] == actual.get("metric") and expected["status"] == actual.get("status"):
                    found = True
                    break
            if not found:
                raise AssertionError(f"Expected SLA '{expected}' not found.")
        return True
