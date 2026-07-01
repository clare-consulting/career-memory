from collections import defaultdict
from datetime import date, datetime
from typing import Dict, List, Optional, Tuple

from schema import CareerEvent


class TimelineBuilder:
    """
    Build and print a chronological timeline from CareerEvent records.
    """

    def __init__(self, events: List[CareerEvent]):
        self.events = events

    def sorted_events(self) -> List[CareerEvent]:
        """
        Return events sorted by event_date, with undated events last.
        """
        return sorted(self.events, key=self._sort_key)

    def grouped_events(self) -> Dict[Optional[date], List[CareerEvent]]:
        """
        Group sorted events by calendar date.
        """
        grouped: Dict[Optional[date], List[CareerEvent]] = defaultdict(list)

        for event in self.sorted_events():
            grouped[self._event_day(event)].append(event)

        return dict(grouped)

    def print_timeline(self) -> None:
        """
        Print a readable chronological career event timeline.
        """
        print("Career Timeline")
        print("=" * 40)

        if not self.events:
            print("No career events found.")
            return

        for event_day, events in self.grouped_events().items():
            print(self._format_day(event_day))

            for event in events:
                print(f"- {self._format_event(event)}")

    def _sort_key(self, event: CareerEvent) -> Tuple[int, datetime]:
        """
        Sort dated events chronologically before undated events.
        """
        if event.event_date is None:
            return (1, datetime.max)

        return (0, event.event_date)

    def _event_day(self, event: CareerEvent) -> Optional[date]:
        """
        Return the calendar date for an event, if present.
        """
        if event.event_date is None:
            return None

        return event.event_date.date()

    def _format_day(self, event_day: Optional[date]) -> str:
        """
        Format a timeline group heading.
        """
        if event_day is None:
            return "Undated"

        return event_day.isoformat()

    def _format_event(self, event: CareerEvent) -> str:
        """
        Format one CareerEvent for timeline output.
        """
        parts = [
            event.interaction_type,
            event.subject or "No subject",
        ]

        if event.agency:
            parts.append(f"Agency: {event.agency}")

        if event.client:
            parts.append(f"Client: {event.client}")

        return " | ".join(parts)
