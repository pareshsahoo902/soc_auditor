from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from mock_simulation.scenarios.schema import UnifiedEvent
from mock_simulation.timelines.engine import TimelineEngine
from faker import Faker

class BaseScenario(ABC):
    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
        self.faker = Faker()
        if seed is not None:
            Faker.seed(seed)
            self.faker.seed_instance(seed)

    @abstractmethod
    def generate_events(self, timeline: TimelineEngine, org_id: str) -> List[UnifiedEvent]:
        """
        Generates the events for this scenario and advances the timeline appropriately.
        """
        pass

    @abstractmethod
    def expected_findings(self) -> List[Dict[str, Any]]:
        """
        Returns the expected governance findings for this scenario.
        """
        pass

    @abstractmethod
    def expected_graph(self) -> List[Dict[str, Any]]:
        """
        Returns the expected evidence graph relationships.
        """
        pass

    @abstractmethod
    def expected_slas(self) -> List[Dict[str, Any]]:
        """
        Returns expected SLA outcomes.
        """
        pass
