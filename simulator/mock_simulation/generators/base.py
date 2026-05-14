from typing import Dict, Any, Optional
from mock_simulation.scenarios.schema import UnifiedEvent
from faker import Faker
import random

class GeneratorBase:
    def __init__(self, faker_instance: Faker):
        self.faker = faker_instance
