"""
Recommendation engine — CM-016.

Rules-based only, deliberately (matches the project's stated approach:
rules first, LLM/embeddings later once the event model is stable).

Scope: pick the single most actionable open CareerEvent and describe it
using real fields. No AI, no persistence, no scoring math yet — that's
Opportunity Score, a separate future piece. This just replaces the
hardcoded "Respond to Example Staffing" text with something driven by
whatever real data actually came in today.
"""

from typing import List, Optional

from schema import CareerEvent

# Priority order for "what needs a response." Earlier = more urgent/actionable.
# REJECTION and OUTREACH are intentionally excluded from this list:
# REJECTION needs no action, and OUTREACH is too generic/high-volume to
# single one out as "the" recommendation without more signal than exists
# today (that's exactly the gap Opportunity Score is meant to fill later).
ACTIONABLE_PRIORITY = [
    "INTERVIEW",
    "ASSESSMENT",
    "RTR_REQUEST",
    "RESUME_REQUEST",
    "RATE_NEGOTIATION",
    "SUBMISSION",
    "DL_REQUEST",
    "REFERENCES_REQUEST",
]


class Recommendation:
    def __init__(self, event: CareerEvent, reason_lines: List[str]):
        self.event = event
        self.reason_lines = reason_lines

    @property
    def headline(self) -> str:
        """
        One-line action description, built from real event fields only.
        """
        who = self._describe_sender()
        action = self._describe_action()
        return f"{action} {who}."

    def _describe_sender(self) -> str:
        if self.event.agency:
            return f"from {self.event.agency}"
        if self.event.client:
            return f"about {self.event.client}"
        if self.event.subject:
            # Fallback to a truncated subject line when no structured
            # agency/client was extracted — still real data, not invented.
            subject = self.event.subject.strip()
            if len(subject) > 50:
                subject = subject[:47] + "..."
            return f're: "{subject}"'
        return "from a recruiter contact"

    def _describe_action(self) -> str:
        labels = {
            "INTERVIEW": "Respond about your upcoming interview",
            "ASSESSMENT": "Complete the pending assessment",
            "RTR_REQUEST": "Sign and return the RTR",
            "RESUME_REQUEST": "Send your resume",
            "RATE_NEGOTIATION": "Respond on rate",
            "SUBMISSION": "Follow up on your submission",
            "DL_REQUEST": "Send your driver's license copy",
            "REFERENCES_REQUEST": "Send your references",
        }
        return labels.get(self.event.interaction_type, "Follow up")


class RecommendationEngine:
    """
    Selects the single most actionable CareerEvent from today's loaded events.
    """

    def __init__(self, events: List[CareerEvent]):
        self.events = events

    def get_recommendation(self) -> Optional[Recommendation]:
        """
        Returns a Recommendation for the highest-priority actionable event,
        or None if no actionable events exist (e.g. an inbox with only
        OUTREACH/REJECTION today — a real, valid state, not an error).
        """
        candidate = self._select_candidate()
        if candidate is None:
            return None

        reason_lines = self._build_reason(candidate)
        return Recommendation(candidate, reason_lines)

    def _select_candidate(self) -> Optional[CareerEvent]:
        for interaction_type in ACTIONABLE_PRIORITY:
            matches = [e for e in self.events if e.interaction_type == interaction_type]
            if matches:
                # No event_date populated yet in the current parser, so we
                # can't sort by recency — take the first match in load order.
                # Worth revisiting once event_date extraction exists.
                return matches[0]
        return None

    def _build_reason(self, event: CareerEvent) -> List[str]:
        reasons = []

        type_label = event.interaction_type.replace("_", " ").title()
        reasons.append(f"Interaction type: {type_label}.")

        if event.agency:
            reasons.append(f"Agency: {event.agency}.")
        if event.client:
            reasons.append(f"Client: {event.client}.")
        if event.role_title:
            reasons.append(f"Role: {event.role_title}.")

        if len(reasons) == 1:
            # Only the interaction type was available — say so honestly
            # rather than padding with invented specifics.
            reasons.append("No additional agency, client, or role detail was extracted from this message.")

        return reasons