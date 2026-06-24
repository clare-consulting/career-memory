from classification_rules import classify_email

samples = [
    (
        "RTR Required for Data Engineer",
        "Please send your updated resume and right to represent."
    ),
    (
        "Interview Scheduled",
        "The client would like to schedule an interview."
    ),
    (
        "Coding Assessment",
        "Please complete the attached coding challenge."
    ),
    (
        "Thank you for your interest",
        "The client has decided to move forward with another candidate."
    ),
]

for subject, body in samples:
    result = classify_email(subject, body)
    print(f"{subject} -> {result}")