from typing import List

from schema import CareerEvent
from connectors.base import CareerConnector


class DiceConnector(CareerConnector):
    source_name = "dice"

    def load_events(self) -> List[CareerEvent]:
        """
        Future: load Dice job alerts or exports.
        """
        return []