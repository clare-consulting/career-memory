from typing import List

from schema import RecruiterInteraction
from connectors.base import CareerConnector


class DiceConnector(CareerConnector):
    source_name = "dice"

    def load_events(self) -> List[RecruiterInteraction]:
        """
        Future: load Dice job alerts or exports.
        """
        return []