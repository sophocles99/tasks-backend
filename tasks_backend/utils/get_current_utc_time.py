from datetime import UTC, datetime


def get_current_utc_time():
    return datetime.now(UTC)
