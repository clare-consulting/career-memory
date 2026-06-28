from typing import List

from schema import CareerEvent

from connectors.gmail import GmailConnector
from connectors.linkedin import LinkedInConnector
from connectors.dice import DiceConnector
from connectors.clearancejobs import ClearanceJobsConnector


class ConnectorManager:

    def __init__(self):

        self.connectors = [
            GmailConnector(),
            LinkedInConnector(),
            DiceConnector(),
            ClearanceJobsConnector()
        ]

    def load_all_events(self) -> List[CareerEvent]:

        events = []

        for connector in self.connectors:

            print(f"Loading {connector.source_name}...")

            events.extend(connector.load_events())

        return events