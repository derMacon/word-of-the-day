from datetime import timezone, timedelta, datetime

DATETIME_FORMAT_STRING = '%Y-%m-%d %H:%M:%S'
BERLIN_TIMEZONE = timezone(timedelta(hours=1))


def now():
    # return datetime.now(BERLIN_TIMEZONE).strftime(DATETIME_FORMAT_STRING)
    return datetime.now(BERLIN_TIMEZONE)


def parse_datetime_from_string(date_string):
    # Parse the string into a naive datetime object
    naive_datetime = datetime.strptime(date_string, DATETIME_FORMAT_STRING)

    # Assign the Berlin timezone to the naive datetime object
    berlin_datetime = naive_datetime.replace(tzinfo=BERLIN_TIMEZONE)

    return berlin_datetime

