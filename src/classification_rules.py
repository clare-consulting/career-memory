"""
Deterministic recruiter email classification — CM-014.

Design notes:
- Rules are checked in priority order, not scanned independently. Real
  recruiter emails overlap categories constantly (an RTR request usually
  also asks for a resume; a submission email often mentions a rate).
  Priority order resolves the overlap toward the more specific/urgent
  signal rather than whichever category happens to run first.
- Each category is a list of regex patterns, not exact phrases. Real inbox
  phrasing varies ("send your resume" vs "share an updated resume" vs
  "can you forward your resume") far more than a single fixture email does.
- OUTREACH remains the fallback when nothing else matches — that's correct
  behavior, not a sign the parser is broken. The bug we're fixing is
  everything falling through to it, not the existence of the fallback.
"""

import re

# Priority order matters. Checked top to bottom; first match wins.
# Reasoning for the order:
#   1. RTR / DL / REFERENCES — highly specific document requests, rarely
#      ambiguous with anything else.
#   2. INTERVIEW / ASSESSMENT — scheduling language is distinctive.
#   3. REJECTION — must come before SUBMISSION/RESUME_REQUEST, since a
#      rejection email often references a submission that already happened
#      ("we submitted you but the client moved forward with someone else").
#   4. RATE_NEGOTIATION — distinctive enough to check before the broader
#      SUBMISSION/RESUME_REQUEST buckets.
#   5. SUBMISSION — "we submitted your profile" is a different lifecycle
#      stage than a raw resume request, so it's checked first.
#   6. RESUME_REQUEST — broad, checked last among the specific types since
#      "resume" appears as a side mention in several other categories.
CLASSIFICATION_RULES: list[tuple[str, list[str]]] = [
    ("RTR_REQUEST", [
        r"\bright to represent\b",
        r"\brtr\b",
        r"\bsign(?:ed)?\s+(?:the\s+)?rtr\b",
    ]),
    ("DL_REQUEST", [
        r"\bdriver'?s?\s+licen[sc]e\b",
        r"\bdl\s+copy\b",
        r"\bcopy of your (?:dl|driver'?s?\s+licen[sc]e)\b",
    ]),
    ("REFERENCES_REQUEST", [
        r"\breference\s+check\b",
        r"\bprovide\s+(?:2|3|two|three|a\s+few)?\s*references\b",
        r"\bprofessional\s+references\b",
        r"\blist\s+of\s+references\b",
    ]),
    ("INTERVIEW", [
        r"\binterview\b",
        r"\bphone\s+screen\b",
        r"\bschedule\s+(?:a\s+)?call\b",
        r"\bmeet\s+with\s+the\s+client\b",
        r"\bavailab(?:le|ility)\s+for\s+a\s+call\b",
    ]),
    ("ASSESSMENT", [
        r"\bassessment\b",
        r"\bcoding\s+(?:challenge|test|assessment)\b",
        r"\btechnical\s+screen\b",
        r"\bhackerrank\b",
        r"\bcodesignal\b",
        r"\btake[- ]home\s+(?:test|assignment|project)\b",
    ]),
    ("REJECTION", [
        r"\bunfortunately\b",
        r"\bnot\s+selected\b",
        r"\bmove(?:d)?\s+forward\s+with\s+(?:another|a\s+different)\s+candidate\b",
        r"\bposition\s+(?:has\s+been\s+)?filled\b",
        r"\bno\s+longer\s+(?:available|accepting)\b",
        r"\bdecided\s+to\s+go\s+(?:with|in\s+a\s+different\s+direction)\b",
        r"\bwill\s+not\s+be\s+moving\s+forward\b",
    ]),
    ("RATE_NEGOTIATION", [
        r"\b(?:bill|pay|hourly)\s+rate\b",
        r"\brate\s+expect(?:ation|ed)\b",
        r"\bwhat'?s?\s+your\s+rate\b",
        r"\bcompensation\s+expect",
        r"\bsalary\s+expect",
        r"\bnegotiate\s+(?:the\s+)?rate\b",
    ]),
    ("SUBMISSION", [
        r"\bsubmitted\s+your\s+(?:profile|resume)\b",
        r"\bsubmit(?:ting|ted)?\s+you\s+(?:to|for)\b",
        r"\bpresented\s+you(?:r\s+profile)?\s+to\s+the\s+client\b",
        r"\bshared\s+your\s+profile\s+with\s+the\s+client\b",
        r"\byour\s+profile\s+has\s+been\s+submitted\b",
    ]),
    ("RESUME_REQUEST", [
        r"\bsend\s+(?:over\s+)?(?:your|an?\s+updated)\s+resume\b",
        r"\bshare\s+(?:your|an?\s+updated)\s+resume\b",
        r"\bforward\s+(?:your|an?\s+updated)\s+resume\b",
        r"\bupdated\s+(?:copy\s+of\s+your\s+)?resume\b",
        r"\bcan\s+you\s+send\s+(?:me\s+)?(?:your\s+)?resume\b",
    ]),
]


def classify_email(subject: str, body: str) -> str:
    """
    Classify a recruiter email into one interaction type. Deterministic,
    rule-based, no AI. Falls back to OUTREACH when nothing matches.
    """
    text = f"{subject} {body}".lower()

    for label, patterns in CLASSIFICATION_RULES:
        for pattern in patterns:
            if re.search(pattern, text):
                return label

    return "OUTREACH"


# ---------------------------------------------------------------------------
# Validation samples — realistic recruiter phrasing, not the same exact
# strings used in the regex patterns above. The point is to catch overfit
# rules that only match their own wording.
# ---------------------------------------------------------------------------

VALIDATION_CASES: list[tuple[str, str, str, str]] = [
    (
        "RTR_REQUEST",
        "RTR Required for Data Engineer",
        "Please send your updated resume and right to represent so we can submit you today.",
        "Existing sample fixture case, should still pass.",
    ),
    (
        "RTR_REQUEST",
        "Quick RTR before submission",
        "Can you sign the RTR attached so we can move forward with your submission?",
        "RTR mentioned without the full phrase 'right to represent'.",
    ),
    (
        "DL_REQUEST",
        "Need a copy of your license",
        "Client requires a copy of your driver's license before onboarding can start.",
        "DL request phrased naturally, not as 'DL request'.",
    ),
    (
        "REFERENCES_REQUEST",
        "Reference check",
        "Could you provide 3 professional references before Friday?",
        "References request with a specific count.",
    ),
    (
        "INTERVIEW",
        "Interview Scheduled",
        "The client would like to schedule an interview this week.",
        "Existing sample fixture case, should still pass.",
    ),
    (
        "INTERVIEW",
        "Availability for a call",
        "Are you available for a call with the hiring manager tomorrow afternoon?",
        "Interview-adjacent language without the word 'interview'.",
    ),
    (
        "ASSESSMENT",
        "Coding challenge invite",
        "Please complete the HackerRank assessment within 48 hours.",
        "Assessment phrased via a named platform.",
    ),
    (
        "REJECTION",
        "Update on your application",
        "Unfortunately the client has decided to move forward with another candidate.",
        "Classic rejection phrasing.",
    ),
    (
        "REJECTION",
        "Role update",
        "This position has been filled, but we'll keep your resume on file.",
        "Rejection without the word 'unfortunately'; also mentions resume, "
        "should NOT be misclassified as RESUME_REQUEST.",
    ),
    (
        "RATE_NEGOTIATION",
        "Quick question on rate",
        "What's your expected hourly rate for this contract role?",
        "Rate negotiation phrased as a question.",
    ),
    (
        "SUBMISSION",
        "You've been submitted",
        "We submitted your profile to the client this morning, will update you soon.",
        "Submission lifecycle stage, not a request for anything.",
    ),
    (
        "RESUME_REQUEST",
        "Quick resume request",
        "Can you send me an updated resume for this role when you get a chance?",
        "Resume request without RTR or submission context.",
    ),
    (
        "OUTREACH",
        "New opportunity - Senior Data Engineer",
        "We have an exciting new contract opportunity that matches your background.",
        "Generic first-contact outreach, no other category should fire.",
    ),
]


def run_validation() -> bool:
    """
    Runs all validation cases and prints pass/fail per case.
    Returns True if all cases passed.
    """
    all_passed = True
    print(f"Running {len(VALIDATION_CASES)} classification validation cases\n")

    for expected, subject, body, note in VALIDATION_CASES:
        actual = classify_email(subject, body)
        passed = actual == expected
        all_passed = all_passed and passed

        status = "PASS" if passed else "FAIL"
        print(f"[{status}] expected={expected} actual={actual}")
        print(f"       subject: {subject}")
        print(f"       note: {note}")
        if not passed:
            print(f"       body: {body}")
        print()

    summary = "ALL PASSED" if all_passed else "SOME FAILED"
    print(f"--- {summary} ({sum(1 for e, s, b, _ in VALIDATION_CASES if classify_email(s, b) == e)}/{len(VALIDATION_CASES)}) ---")
    return all_passed


if __name__ == "__main__":
    run_validation()