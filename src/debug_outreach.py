"""
Debug helper — not part of the product pipeline.

Prints subject + body/snippet for every real Gmail CareerEvent currently
classified as OUTREACH, so you can eyeball whether classification_rules.py
is missing real phrasing patterns.

Run from project root:
    python src/debug_outreach.py
"""

from connector_manager import ConnectorManager
from source import Source


def main() -> None:
    manager = ConnectorManager()
    events = manager.load_all_events()

    outreach_gmail_events = [
        e for e in events
        if e.interaction_type == "OUTREACH" and e.source == Source.GMAIL
    ]

    print(f"\n{len(outreach_gmail_events)} Gmail events classified as OUTREACH\n")
    print("=" * 60)

    for i, event in enumerate(outreach_gmail_events, start=1):
        print(f"\n[{i}] Subject: {event.subject}")
        print(f"    Body/snippet: {event.body}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()