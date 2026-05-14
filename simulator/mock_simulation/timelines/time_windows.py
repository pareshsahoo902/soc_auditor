from datetime import datetime, timedelta

class TimeWindowUtils:
    @staticmethod
    def within_sla(event_time_iso: str, sla_limit_iso: str) -> bool:
        """
        Determines if an event occurred within the SLA limit.
        """
        event_time = datetime.fromisoformat(event_time_iso.replace('Z', '+00:00'))
        sla_limit = datetime.fromisoformat(sla_limit_iso.replace('Z', '+00:00'))
        return event_time <= sla_limit

    @staticmethod
    def outside_sla(event_time_iso: str, sla_limit_iso: str) -> bool:
        """
        Determines if an event occurred outside the SLA limit.
        """
        return not TimeWindowUtils.within_sla(event_time_iso, sla_limit_iso)

    @staticmethod
    def escalation_delay(creation_time_iso: str, escalation_time_iso: str) -> float:
        """
        Returns the delay in seconds between creation and escalation.
        """
        creation_time = datetime.fromisoformat(creation_time_iso.replace('Z', '+00:00'))
        escalation_time = datetime.fromisoformat(escalation_time_iso.replace('Z', '+00:00'))
        delay = escalation_time - creation_time
        return delay.total_seconds()
