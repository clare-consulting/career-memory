from typing import List

from schema import RecruiterInteraction
from connectors.base import CareerConnector


class LinkedInConnector(CareerConnector):
    source_name = "linkedin"

    def load_events(self) -> List[RecruiterInteraction]:
        """
        Future: load LinkedIn message exports.
        """
        return []