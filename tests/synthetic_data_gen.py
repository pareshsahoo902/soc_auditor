import json
import uuid
from datetime import datetime, timedelta

def generate_fake_incident():
    return {
        "event_id": f"INC-{uuid.uuid4().hex[:6]}",
        "source": "jira",
        "event_type": "incident_updated",
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": {
            "severity": "high",
            "root_cause": "Database connection pool exhausted.",
            "remediation": "Increased pool size."
        }
    }

if __name__ == "__main__":
    incidents = [generate_fake_incident() for _ in range(5)]
    with open("tests/synthetic_dataset.json", "w") as f:
        json.dump(incidents, f, indent=2)
    print("Generated synthetic dataset.")
