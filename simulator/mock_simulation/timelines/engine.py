import time
from typing import List, Callable, Dict, Any
from datetime import datetime, timedelta

from mock_simulation.scenarios.schema import UnifiedEvent

class TimelineEngine:
    def __init__(self, start_time_iso: str):
        self.current_time = datetime.fromisoformat(start_time_iso.replace('Z', '+00:00'))
        self.events: List[UnifiedEvent] = []

    def get_current_time_iso(self) -> str:
        return self.current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    def advance_time(self, seconds: int = 0, minutes: int = 0, hours: int = 0):
        self.current_time += timedelta(seconds=seconds, minutes=minutes, hours=hours)

    def record_event(self, event: UnifiedEvent):
        self.events.append(event)

    def get_events(self) -> List[UnifiedEvent]:
        # Events might have been added out of order due to generation logic, so we sort them
        return sorted(self.events, key=lambda e: e.timestamp)
