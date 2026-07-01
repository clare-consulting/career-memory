import json
from pathlib import Path
from typing import Any, Dict, List

from schema import CareerEvent
from source import Source
from connectors.base import CareerConnector


DEFAULT_SAMPLE_PATH = (
    Path(__file__).resolve().parents[2] / "sample_data" / "redacted_threads.json"
)


class SampleDataConnector(CareerConnector):
    source_name = "sample_data"

    def __init__(self, sample_path: Path = DEFAULT_SAMPLE_PATH):
        self.sample_path = sample_path

    def load_events(self) -> List[CareerEvent]:
        """
        Load redacted sample career events from local JSON data.
        """
        records = self._load_records()

        return [self._record_to_event(record) for record in records]

    def _load_records(self) -> List[Dict[str, Any]]:
        """
        Read redacted sample thread records from disk.
        """
        with self.sample_path.open("r", encoding="utf-8") as sample_file:
            records = json.load(sample_file)

        if not isinstance(records, list):
            raise ValueError("Sample data must contain a list of records.")

        return records

    def _record_to_event(self, record: Dict[str, Any]) -> CareerEvent:
        """
        Convert one redacted sample record into a CareerEvent.
        """
        return CareerEvent(
            source=Source.MANUAL,
            agency=record.get("agency"),
            client=record.get("client"),
            interaction_type=record.get("expected_type", "UNKNOWN"),
            subject=record.get("subject"),
            body=record.get("body"),
            notes="Loaded from sample_data/redacted_threads.json",
        )
