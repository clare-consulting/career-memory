from abc import ABC, abstractmethod
from typing import List

from schema import RecruiterInteraction


class CareerConnector(ABC):
    """
    Base interface for all Career Memory data connectors.
    """

    source_name: str

    @abstractmethod
    def load_events(self) -> List[RecruiterInteraction]:
        """
        Load career-related events from a source system.
        """
        raise NotImplementedError