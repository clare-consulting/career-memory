import re
from typing import Any, Dict, List, Optional

from connectors.gmail_auth import get_gmail_service

# Matches the email address inside a From header, whether it's a bare
# address ("me@example.com") or a display-name form ("Name <me@example.com>").
_EMAIL_PATTERN = re.compile(r"[\w.+\-]+@[\w\-]+\.[\w.\-]+")

# v1 recruiter query. Deliberately broad — tune once this has run against a
# real inbox. Widening/narrowing this string is expected to be an ongoing
# tuning process, not a one-time decision.
DEFAULT_RECRUITER_QUERY = (
    'newer_than:180d ('
    'recruiter OR recruiting OR interview OR "right to represent" OR RTR OR '
    '"submit your resume" OR "updated resume" OR "coding assessment" OR '
    '"technical screen" OR "hiring manager" OR contract OR W2 OR C2C'
    ')'
)


class GmailClient:
    """
    Thin client abstraction over the Gmail API.

    Scope, intentionally narrow (CM-013): search + return message metadata
    only. No full-body parsing beyond what Gmail's metadata format and
    snippet already provide. No persistence, no classification.
    """

    def __init__(self) -> None:
        """
        Initialize the Gmail client. Auth happens lazily on first API call,
        not here, so constructing a GmailClient never triggers a browser
        OAuth flow by itself.
        """
        self._service = None
        self._authenticated_email: Optional[str] = None

    @property
    def service(self):
        if self._service is None:
            self._service = get_gmail_service()
        return self._service

    @property
    def authenticated_email(self) -> Optional[str]:
        """
        Email address of the authenticated Gmail account, used to detect
        self-sent messages (CM-015). Fetched once and cached; returns None
        if the profile call fails, in which case self-sent filtering is
        skipped rather than raising — a filtering feature shouldn't break
        message fetching if it can't determine identity.
        """
        if self._authenticated_email is None:
            try:
                profile = self.service.users().getProfile(userId="me").execute()
                self._authenticated_email = profile.get("emailAddress", "").lower() or None
            except Exception:
                self._authenticated_email = None
        return self._authenticated_email

    def _is_self_sent(self, message: Dict[str, Any]) -> bool:
        """
        Returns True if the message's From header matches the authenticated
        account (CM-015) — i.e. it's the user's own reply, not recruiter mail.
        """
        if not self.authenticated_email:
            return False

        headers = message.get("payload", {}).get("headers", [])
        from_value = next(
            (h.get("value", "") for h in headers if h.get("name", "").lower() == "from"),
            "",
        )
        match = _EMAIL_PATTERN.search(from_value)
        if not match:
            return False

        return match.group(0).lower() == self.authenticated_email

    def list_messages(
        self, query: str = DEFAULT_RECRUITER_QUERY, max_results: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Return Gmail message metadata matching a search query, excluding
        messages sent by the authenticated user (CM-015 — self-sent replies
        inside recruiter threads aren't recruiter outreach).

        Each returned dict has the shape GmailConnector already expects:
        - id, threadId
        - snippet
        - payload.headers (Subject, From, Date)

        format='metadata' is used deliberately so full message bodies are
        never fetched at this stage.

        Note: max_results caps the initial Gmail search, before self-sent
        filtering. If several matches turn out to be self-sent, the returned
        list will be shorter than max_results rather than backfilled — fine
        for MVP, worth revisiting if this ever needs an exact count.
        """
        results = (
            self.service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )
        refs = results.get("messages", [])

        messages = [self.get_message(ref["id"]) for ref in refs]
        return [m for m in messages if not self._is_self_sent(m)]

    def get_message(self, message_id: str) -> Dict[str, Any]:
        """
        Return one Gmail message by message ID, metadata only.
        """
        return (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="metadata",
                metadataHeaders=["Subject", "From", "Date"],
            )
            .execute()
        )