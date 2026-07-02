import re
from typing import Dict, Optional

from classification_rules import classify_email


class RecruiterEmailParser:
    """
    Deterministically parse recruiter email text into CareerEvent fields.
    """

    def parse(self, subject: str, body: str) -> Dict[str, Optional[str]]:
        """
        Extract supported CareerEvent fields from recruiter email text.
        """
        text = self._combined_text(subject, body)

        return {
            "interaction_type": classify_email(subject, body),
            "agency": self._extract_agency(text),
            "role_title": self._extract_role_title(text),
            "client": self._extract_client(text),
        }

    def _combined_text(self, subject: str, body: str) -> str:
        """
        Combine subject and body into a normalized parsing target.
        """
        return f"{subject}\n{body}".strip()

    def _extract_agency(self, text: str) -> Optional[str]:
        """
        Extract staffing agency names from common recruiter phrases.
        """
        patterns = [
            r"\bfrom\s+(?P<value>[A-Z][A-Za-z0-9&_,'\- ]+?)(?:\.|,|\n|$)",
            r"\bat\s+(?P<value>[A-Z][A-Za-z0-9&_,'\- ]+?(?:Staffing|Solutions|Recruiting|Consulting|Technologies|Tech|Group|LLC|Inc\.?))\b",
            r"\bagency\s*[:\-]\s*(?P<value>[^\n.]+)",
        ]

        return self._first_match(text, patterns)

    def _extract_role_title(self, text: str) -> Optional[str]:
        """
        Extract a role title from common job opportunity phrasing.
        """
        patterns = [
            r"\brole\s*[:\-]\s*(?P<value>[^\n.]+)",
            r"\bposition\s*[:\-]\s*(?P<value>[^\n.]+)",
            r"\bopportunity\s+(?:for|as)\s+(?P<value>[A-Z][A-Za-z0-9&_,'/+\- ]+?)(?:\.|,|\n|$)",
            r"\blooking for (?:an? )?(?P<value>[A-Z][A-Za-z0-9&_,'/+\- ]+?)(?:\.|,|\n|$)",
        ]

        return self._first_match(text, patterns)

    def _extract_client(self, text: str) -> Optional[str]:
        """
        Extract a client name only when it is clearly labeled.
        """
        patterns = [
            r"\bclient\s*[:\-]\s*(?P<value>[^\n.]+)",
            r"\bend client\s+(?:is|:)\s*(?P<value>[^\n.]+)",
            r"\bwith\s+client\s+(?P<value>[A-Z][A-Za-z0-9&_,'\- ]+?)(?:\.|,|\n|$)",
        ]

        return self._first_match(text, patterns)

    def _first_match(self, text: str, patterns: list[str]) -> Optional[str]:
        """
        Return the first cleaned regex match from a list of patterns.
        """
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)

            if not match:
                continue

            value = self._clean_value(match.group("value"))

            if value:
                return value

        return None

    def _clean_value(self, value: str) -> Optional[str]:
        """
        Normalize extracted text values.
        """
        cleaned = re.sub(r"\s+", " ", value).strip(" .,-")

        if not cleaned:
            return None

        return cleaned
