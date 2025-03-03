import datetime


def utcnow() -> datetime:
    tz_offset = datetime.timedelta(hours=3)
    tz_moscow = datetime.timezone(tz_offset)
    moscow_time = datetime.datetime.now(tz_moscow)
    return moscow_time.replace(tzinfo=None)
