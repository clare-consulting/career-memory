from typing import List

from schema import RecruiterInteraction
from connectors.base import CareerConnector


class GmailConnector(CareerConnector):
    source_name = "gmail"

    def load_events(self) -> List[RecruiterInteraction]:
        """
        Future: load recruiter emails from Gmail.
        """
        return []