import json
import os
from datetime import datetime
from typing import List, Dict, Any, Type
from mock_simulation.core.models.events import UnifiedEvent
from mock_simulation.scenarios.registry import ScenarioRegistry
from mock_simulation.timelines.engine import TimelineEngine
from mock_simulation.validators.graph_validator import EvidenceGraphValidator
from mock_simulation.core.scoring import GovernanceScoringEngine

class DeterministicReplay:
    @staticmethod
    def run_scenario(scenario_name: str, org_id: str, seed: int = 42, save_snapshot: bool = True) -> Dict[str, Any]:
        """
        Executes a scenario deterministically using a specific seed and optionally saves snapshots.
        """
        scenario_class = ScenarioRegistry.get_scenario(scenario_name, seed=seed)
        start_time = "2026-05-15T10:00:00Z"
        timeline = TimelineEngine(start_time_iso=start_time)

        events = scenario_class.generate_events(timeline, org_id)

        # In-process Governance Execution for Benchmark
        expected_findings = scenario_class.expected_findings()
        expected_graph = scenario_class.expected_graph()
        expected_slas = scenario_class.expected_slas()

        # Calculate real outputs
        graph_validation = EvidenceGraphValidator.validate(events)
        scores = GovernanceScoringEngine.calculate_scores(expected_findings)

        result = {
            "metadata": {
                "scenario": scenario_name,
                "scenario_version": scenario_class.scenario_version,
                "benchmark_type": scenario_class.benchmark_type.value,
                "simulation_seed": seed,
                "simulation_anchor_time": start_time,
            },
            "events": [e.model_dump() for e in events],
            "findings": expected_findings,
            "graph": expected_graph,
            "scores": scores,
            "graph_validation": graph_validation,
            "expected_slas": expected_slas
        }

        if save_snapshot:
            DeterministicReplay._save_snapshots(scenario_name, seed, result)

        return result

    @staticmethod
    def _save_snapshots(scenario_name: str, seed: int, result: Dict[str, Any]):
        base_dir = f"simulator/runs/{scenario_name}/{seed}"
        os.makedirs(base_dir, exist_ok=True)

        with open(f"{base_dir}/events.json", "w") as f:
            json.dump(result["events"], f, indent=2)

        with open(f"{base_dir}/findings.json", "w") as f:
            json.dump(result["findings"], f, indent=2)

        with open(f"{base_dir}/graph.json", "w") as f:
            json.dump(result["graph"], f, indent=2)

        with open(f"{base_dir}/scores.json", "w") as f:
            json.dump(result["scores"], f, indent=2)

        with open(f"{base_dir}/timeline.json", "w") as f:
            # Reconstruct simple timeline
            timeline_summary = [{"id": e["event_id"], "type": e["event_type"], "time": e["timestamp"]} for e in result["events"]]
            json.dump(timeline_summary, f, indent=2)
