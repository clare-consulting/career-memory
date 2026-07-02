from typing import Any, Dict, List


class GmailClient:
    """
    Thin client abstraction for future Gmail API access.

    This class intentionally does not implement OAuth or call Gmail yet. It
    exists so connectors can later depend on a small, testable client surface.
    """

    def __init__(self) -> None:
        """
        Initialize the Gmail client placeholder.
        """
        # TODO: Add OAuth credential setup when Gmail authentication is defined.
        self.service = None

    def list_messages(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Return Gmail message metadata matching a search query.
        """
        # TODO: Call Gmail users.messages.list with query and max_results.
        return []

    def get_message(self, message_id: str) -> Dict[str, Any]:
        """
        Return one Gmail message by message ID.
        """
        # TODO: Call Gmail users.messages.get for the provided message_id.
        return {}
