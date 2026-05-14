from typing import List, Dict, Any, Optional
from mock_simulation.scenarios.base import BaseScenario
from mock_simulation.core.models.events import UnifiedEvent
from mock_simulation.scenarios.registry import ScenarioRegistry
from mock_simulation.timelines.engine import TimelineEngine
from mock_simulation.core.models.governance import BenchmarkType

class CompositeScenario(BaseScenario):
    """
    Enables composition of multiple scenarios into one large simulation trace.
    """
    def __init__(self, scenario_names: List[str], seed: Optional[int] = None):
        super().__init__(seed=seed)
        self.scenario_names = scenario_names
        self.scenarios = [ScenarioRegistry.get_scenario(name, seed=self.seed) for name in scenario_names]

        self.name = f"Composite: {' + '.join(scenario_names)}"
        self.benchmark_type = BenchmarkType.SCALE

    def generate_events(self, timeline: TimelineEngine, org_id: str) -> List[UnifiedEvent]:
        # Generate events for each scenario sequentially on the same timeline
        for scenario in self.scenarios:
            scenario.generate_events(timeline, org_id)
            # Add some buffer time between scenarios
            timeline.advance_time(hours=1)
        return timeline.get_events()

    def expected_findings(self) -> List[Dict[str, Any]]:
        findings = []
        for scenario in self.scenarios:
            findings.extend(scenario.expected_findings())
        return findings

    def expected_graph(self) -> List[Dict[str, Any]]:
        graph = []
        for scenario in self.scenarios:
            graph.extend(scenario.expected_graph())
        return graph

    def expected_slas(self) -> List[Dict[str, Any]]:
        slas = []
        for scenario in self.scenarios:
            slas.extend(scenario.expected_slas())
        return slas
