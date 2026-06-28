from typing import List

from schema import CareerEvent
from connectors.base import CareerConnector


class GmailConnector(CareerConnector):
    source_name = "gmail"

    def load_events(self) -> List[CareerEvent]:
        """
        Future: load recruiter emails from Gmail.
        """
        return []