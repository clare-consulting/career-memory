from enum import Enum


class Source(str, Enum):
    GMAIL = "gmail"
    LINKEDIN = "linkedin"
    DICE = "dice"
    CLEARANCEJOBS = "clearancejobs"
    MANUAL = "manual"