import datetime
import re

t = re.compile(".*chosen.*")
print(type(t))

print(re.search(t, "IchosenYou"))
print(re.match(t, "IchosenYou"))

t = ["str", "int"]
print(type(t))

t = True
print(type(t))
print(type(t)=='bool')
print(isinstance(t, bool))

d = datetime.datetime.utcnow()
#d = datetime.datetime.now(tz=datetime.timezone.tzname("Europe")).strftime("%Y-%m-%d %H:%M:%S")
print(d.strftime("%Y-%m-%d %H:%M:%S"))

t = datetime.timedelta(hours=4)
print(t)
d2 = d + t
print(d2.strftime("%Y-%m-%d %H:%M:%S"))