import datetime

from dateutil.relativedelta import relativedelta

d = datetime.datetime.utcnow()
#d = datetime.datetime.now(tz=datetime.timezone.tzname("Europe")).strftime("%Y-%m-%d %H:%M:%S")
print(d.strftime("%Y-%m-%d %H:%M:%S"))
print(d.strftime("%Y-%m"))

t = datetime.timedelta(hours=5,minutes=30)
t2 = relativedelta(months=3)
print(t)
d2 = d + t
print(d2.strftime("%Y-%m-%d %H:%M:%S"))
d3 = d-t2
print(d3.strftime("%Y-%m"))

d = "2022-12"
print(datetime.datetime.ctime(d))