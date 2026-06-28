from typing import List

from schema import CareerEvent
from connectors.base import CareerConnector


class LinkedInConnector(CareerConnector):
    source_name = "linkedin"

    def load_events(self) -> List[CareerEvent]:
        """
        Future: load LinkedIn message exports.
        """
        return []