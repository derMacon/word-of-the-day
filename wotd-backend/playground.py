from datetime import datetime, timezone, timedelta

ts = '2013-01-12 15:27:43'
f = '%Y-%m-%d %H:%M:%S'
# print(datetime.datetime.strptime(ts, f))
berlin_timezone = timezone(timedelta(hours=1))
print(datetime.now(berlin_timezone).strftime(f))
