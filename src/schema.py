from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from source import Source


@dataclass
class CareerEvent:
    """
    Represents a single career-related event from any supported source.
    """
    # Source metadata
    source: Source
    thread_id: Optional[str] = None
    message_id: Optional[str] = None
    # Which specific account/mailbox this event came from, e.g. a Gmail
    # address. Distinct from `source` (which just says "gmail") — this is
    # what makes multi-mailbox analytics and cross-account dedup possible
    # later. None for sources that don't have a meaningful per-account
    # distinction yet (e.g. sample_data).
    account_label: Optional[str] = None
    # Time
    event_date: Optional[datetime] = None
    # Recruiter information
    recruiter_name: Optional[str] = None
    recruiter_email: Optional[str] = None
    # Company information
    agency: Optional[str] = None
    client: Optional[str] = None
    # Job information
    role_title: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    rate: Optional[str] = None
    # Classification
    interaction_type: str = "UNKNOWN"
    # Outcome
    outcome: str = "UNKNOWN"
    # Original content
    subject: Optional[str] = None
    body: Optional[str] = None
    # Notes
    notes: str = ""