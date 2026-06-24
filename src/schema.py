from dataclasses import dataclass
from datetime import datetime


@dataclass
class RecruiterInteraction:
    recruiter_name: str
    agency: str
    client: str
    role_title: str
    interaction_type: str
    interaction_date: datetime
    outcome: str
    notes: str = ""