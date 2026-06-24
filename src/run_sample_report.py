import json
from pathlib import Path

from classification_rules import classify_email


def load_samples(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    samples_path = Path("sample_data/redacted_threads.json")
    samples = load_samples(samples_path)

    print("Career Memory Sample Report")
    print("=" * 40)

    for item in samples:
        subject = item["subject"]
        body = item["body"]
        agency = item.get("agency", "UNKNOWN")
        client = item.get("client", "UNKNOWN")

        interaction_type = classify_email(subject, body)

        print(f"Agency: {agency}")
        print(f"Client: {client}")
        print(f"Subject: {subject}")
        print(f"Classified As: {interaction_type}")
        print("-" * 40)


if __name__ == "__main__":
    main()