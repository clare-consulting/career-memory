# src/classification_rules.py

def classify_email(subject: str, body: str):

    text = f"{subject} {body}".lower()

    if "right to represent" in text or "rtr" in text:
        return "RTR_REQUEST"

    if "driver license" in text or "driver's license" in text:
        return "DL_REQUEST"

    if "references" in text:
        return "REFERENCES_REQUEST"

    if "interview" in text:
        return "INTERVIEW"

    if "assessment" in text or "coding challenge" in text:
        return "ASSESSMENT"

    return "OUTREACH"
