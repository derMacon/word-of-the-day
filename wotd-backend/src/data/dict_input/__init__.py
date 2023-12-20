from datetime import timezone, timedelta, datetime

DATETIME_FORMAT_STRING = '%Y-%m-%d %H:%M:%S'
BERLIN_TIMEZONE = timezone(timedelta(hours=1))


def now():
    return datetime.now(BERLIN_TIMEZONE).strftime(DATETIME_FORMAT_STRING)
