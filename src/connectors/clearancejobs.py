from typing import List

from schema import CareerEvent
from connectors.base import CareerConnector


class ClearanceJobsConnector(CareerConnector):
    source_name = "clearancejobs"

    def load_events(self) -> List[CareerEvent]:
        """
        Future: load ClearanceJobs alerts, exports, or manual records.
        """
        return []