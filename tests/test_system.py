import pytest
from services.governance_engine.event_validator import EventValidator
from services.rule_engine.evaluator import RuleEngine

def test_jira_incident_ingestion_validation():
    # TEST CASE 1 - Validation
    payload = {
        "event_id": "JIRA-123",
        "source": "jira",
        "event_type": "incident_updated",
        "timestamp": "2023-10-24T12:00:00Z",
        "metadata": {"severity": "high"}
    }
    event = EventValidator.validate(payload)
    assert event is not None
    assert event.event_id == "JIRA-123"

def test_missing_rca_detection():
    # TEST CASE 5
    rule_engine = RuleEngine()
    event_dict = {
        "event_id": "JIRA-456",
        "event_type": "incident_updated",
        "metadata": {
            "severity": "high",
            "root_cause": "" # Missing
        }
    }
    findings = rule_engine.evaluate(event_dict)
    assert len(findings) > 0
    assert findings[0]["finding"] == "Missing root cause in RCA"

def test_missing_approval_detection():
    # TEST CASE 6
    rule_engine = RuleEngine()
    event_dict = {
        "event_id": "PR-789",
        "event_type": "pr_merged",
        "metadata": {
            "approvals": False
        }
    }
    findings = rule_engine.evaluate(event_dict)
    assert len(findings) > 0
    assert findings[0]["finding"] == "PR merged without approvals"
