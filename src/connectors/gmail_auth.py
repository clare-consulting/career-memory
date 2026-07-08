"""
Gmail OAuth handler for career-memory.

Responsible for one thing: getting an authenticated Gmail API service
object. Token lifecycle (first auth, refresh, re-auth) lives here so the
gmail connector itself can stay focused on fetching + mapping messages.
"""

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Read-only is all the Morning Brief needs. Widening this scope later
# (e.g. to send replies) means users will need to re-consent.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

CREDENTIALS_PATH = Path("credentials.json")   # from Google Cloud Console, gitignored
TOKEN_PATH = Path("token.json")               # generated after first auth, gitignored


def get_gmail_service():
    """
    Returns an authenticated Gmail API service object.

    First run: opens a browser window for the OAuth consent screen.
    Subsequent runs: loads the cached token and refreshes silently if expired.
    """
    creds = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                raise FileNotFoundError(
                    f"Missing {CREDENTIALS_PATH}. Download it from Google Cloud "
                    "Console → Credentials → your OAuth client → Download JSON."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Cache for next run
        TOKEN_PATH.write_text(creds.to_json())

    return build("gmail", "v1", credentials=creds)


if __name__ == "__main__":
    # Quick smoke test: auth successfully and print the authenticated address.
    service = get_gmail_service()
    profile = service.users().getProfile(userId="me").execute()
    print(f"Authenticated as: {profile['emailAddress']}")
