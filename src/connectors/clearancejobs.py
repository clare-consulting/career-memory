from typing import List

from schema import RecruiterInteraction
from connectors.base import CareerConnector


class ClearanceJobsConnector(CareerConnector):
    source_name = "clearancejobs"

    def load_events(self) -> List[RecruiterInteraction]:
        """
        Future: load ClearanceJobs alerts, exports, or manual records.
        """
        return []