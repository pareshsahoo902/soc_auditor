from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from mock_simulation.core.models.events import UnifiedEvent
from mock_simulation.core.models.governance import BenchmarkType
from mock_simulation.timelines.engine import TimelineEngine
from mock_simulation.core.seeded_faker import SeededDataGenerator

class BaseScenario(ABC):
    # Metadata Contracts
    name: str = "Base Scenario"
    description: str = ""
    scenario_version: str = "1.0.0"
    benchmark_type: BenchmarkType = BenchmarkType.HAPPY_PATH
    tags: List[str] = []

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed if seed is not None else 42
        self.faker = SeededDataGenerator(self.seed)

    @abstractmethod
    def generate_events(self, timeline: TimelineEngine, org_id: str) -> List[UnifiedEvent]:
        """
        Generates the events for this scenario and advances the timeline appropriately.
        """
        pass

    def expected_findings(self) -> List[Dict[str, Any]]:
        return []

    def expected_graph(self) -> List[Dict[str, Any]]:
        return []

    def expected_slas(self) -> List[Dict[str, Any]]:
        return []

    def expected_scores(self) -> Dict[str, float]:
        return {}

    def expected_failures(self) -> List[Dict[str, Any]]:
        return []
