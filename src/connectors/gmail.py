from typing import List

from schema import CareerEvent
from connectors.base import CareerConnector


class GmailConnector(CareerConnector):
    source_name = "gmail"

    def load_events(self) -> List[CareerEvent]:
        """
        Load career-related events from Gmail.

        Authentication and Gmail API access are intentionally not implemented yet.
        """
        # TODO: Integrate Gmail API client after authentication is defined.
        # TODO: Fetch candidate recruiter email threads/messages from Gmail.
        # TODO: Map Gmail messages into CareerEvent instances.
        return []
