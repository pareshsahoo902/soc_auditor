from typing import Dict, Any, Optional
from mock_simulation.core.models.events import UnifiedEvent
from mock_simulation.core.seeded_faker import SeededDataGenerator
from mock_simulation.core.id_generator import IDGenerator

class GeneratorBase:
    def __init__(self, faker_instance: SeededDataGenerator):
        self.faker = faker_instance
        self.id_gen = IDGenerator()
