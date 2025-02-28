import datetime


def utcnow() -> datetime:
    return datetime.datetime.now(datetime.timezone.utc)
