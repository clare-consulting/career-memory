import importlib.util
from pathlib import Path
from typing import Any, Dict, List, Optional

from clients.gmail_client import GmailClient
from schema import CareerEvent
from source import Source
from connectors.base import CareerConnector


def _load_recruiter_email_parser() -> Any:
    """
    Load the project parser module without importing Python's stdlib parser.
    """
    parser_path = Path(__file__).resolve().parents[1] / "parser.py"
    spec = importlib.util.spec_from_file_location("career_memory_parser", parser_path)

    if spec is None or spec.loader is None:
        raise ImportError("Unable to load RecruiterEmailParser.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.RecruiterEmailParser


RecruiterEmailParser = _load_recruiter_email_parser()


class GmailConnector(CareerConnector):
    source_name = "gmail"

    def __init__(
        self,
        client: Optional[GmailClient] = None,
        parser: Optional[Any] = None,
    ) -> None:
        """
        Initialize the Gmail connector with client and parser dependencies.
        """
        self.client = client or GmailClient()
        self.parser = parser or RecruiterEmailParser()

    def load_events(self) -> List[CareerEvent]:
        """
        Load career-related events from Gmail.
        """
        messages = self.client.list_messages(query="recruiter", max_results=20)

        return [self._message_to_event(message) for message in messages]

    def _message_to_event(self, message: Dict[str, Any]) -> CareerEvent:
        """
        Convert Gmail message metadata into a CareerEvent.
        """
        subject = self._extract_subject(message)
        body = self._extract_body(message)
        parsed_fields = self.parser.parse(subject, body)

        return CareerEvent(
            source=Source.GMAIL,
            thread_id=self._get_optional_text(message, "threadId", "thread_id"),
            message_id=self._get_optional_text(message, "id", "message_id"),
            # CM-017: tag each event with which mailbox it came from.
            # Uses the already-cached authenticated_email from GmailClient
            # (added in CM-015 for self-sent filtering) — no new API call.
            account_label=self.client.authenticated_email,
            subject=subject,
            body=body,
            interaction_type=parsed_fields.get("interaction_type") or "UNKNOWN",
            agency=parsed_fields.get("agency"),
            client=parsed_fields.get("client"),
            role_title=parsed_fields.get("role_title"),
            notes="Mapped from Gmail metadata; full Gmail parsing is not implemented yet.",
        )

    def _extract_subject(self, message: Dict[str, Any]) -> str:
        """
        Extract an available subject from Gmail metadata.
        """
        direct_subject = self._get_optional_text(message, "subject")

        if direct_subject:
            return direct_subject

        return self._get_header(message, "Subject") or ""

    def _extract_body(self, message: Dict[str, Any]) -> str:
        """
        Extract available message text from Gmail metadata.
        """
        return self._get_optional_text(message, "body", "snippet", "text") or ""

    def _get_optional_text(self, message: Dict[str, Any], *keys: str) -> Optional[str]:
        """
        Return the first non-empty string value for the provided keys.
        """
        for key in keys:
            value = message.get(key)

            if isinstance(value, str) and value:
                return value

        return None

    def _get_header(self, message: Dict[str, Any], header_name: str) -> Optional[str]:
        """
        Return a header value from Gmail-style payload metadata.
        """
        payload = message.get("payload")

        if not isinstance(payload, dict):
            return None

        headers = payload.get("headers")

        if not isinstance(headers, list):
            return None

        for header in headers:
            if not isinstance(header, dict):
                continue
            if header.get("name", "").lower() == header_name.lower():
                value = header.get("value")

                if isinstance(value, str) and value:
                    return value

        return None