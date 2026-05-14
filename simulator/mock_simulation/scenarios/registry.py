from typing import Dict, Type, Optional
from mock_simulation.scenarios.base import BaseScenario

class ScenarioRegistry:
    _scenarios: Dict[str, Type[BaseScenario]] = {}

    @classmethod
    def register(cls, name: str):
        def wrapper(scenario_class: Type[BaseScenario]):
            cls._scenarios[name] = scenario_class
            return scenario_class
        return wrapper

    @classmethod
    def get_scenario(cls, name: str, seed: Optional[int] = None) -> BaseScenario:
        if name not in cls._scenarios:
            raise ValueError(f"Scenario '{name}' not found in registry.")
        return cls._scenarios[name](seed=seed)

    @classmethod
    def list_scenarios(cls) -> Dict[str, Type[BaseScenario]]:
        return cls._scenarios
