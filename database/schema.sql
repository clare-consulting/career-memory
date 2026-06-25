CREATE TABLE IF NOT EXISTS career_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_date TEXT,
    recruiter_name TEXT,
    recruiter_email TEXT,
    agency TEXT,
    client TEXT,
    role_title TEXT,
    interaction_type TEXT,
    rate TEXT,
    location TEXT,
    outcome TEXT,
    notes TEXT,
    source_subject TEXT,
    source_thread_id TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);