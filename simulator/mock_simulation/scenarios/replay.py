from typing import List, Dict, Any, Type
from mock_simulation.scenarios.schema import UnifiedEvent
from mock_simulation.scenarios.registry import ScenarioRegistry
from mock_simulation.timelines.engine import TimelineEngine

class DeterministicReplay:
    @staticmethod
    def run_scenario(scenario_name: str, org_id: str, seed: int = 42) -> Dict[str, Any]:
        """
        Executes a scenario deterministically using a specific seed.
        """
        scenario_class = ScenarioRegistry.get_scenario(scenario_name, seed=seed)
        timeline = TimelineEngine(start_time_iso="2026-05-15T10:00:00Z")

        events = scenario_class.generate_events(timeline, org_id)

        return {
            "scenario": scenario_name,
            "seed": seed,
            "events": [e.model_dump() for e in events],
            "expected_findings": scenario_class.expected_findings(),
            "expected_graph": scenario_class.expected_graph(),
            "expected_slas": scenario_class.expected_slas()
        }
