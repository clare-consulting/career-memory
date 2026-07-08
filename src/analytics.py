from collections import Counter
from typing import Dict, List

from schema import CareerEvent


class AnalyticsEngine:
    """
    Compute simple aggregate counts for CareerEvent records.
    """

    def __init__(self, events: List[CareerEvent]):
        self.events = events

    def count_by_source(self) -> Dict[str, int]:
        """
        Count career events by source.
        """
        return dict(Counter(event.source.value for event in self.events))

    def count_by_agency(self) -> Dict[str, int]:
        """
        Count career events by agency.
        """
        return self._count_optional_text("agency")

    def count_by_interaction_type(self) -> Dict[str, int]:
        """
        Count career events by interaction type.
        """
        return dict(Counter(event.interaction_type for event in self.events))

    def _count_optional_text(self, field_name: str) -> Dict[str, int]:
        """
        Count non-empty string values for an optional CareerEvent field.
        """
        values = [
            value
            for event in self.events
            if isinstance((value := getattr(event, field_name)), str) and value
        ]

        return dict(Counter(values))
