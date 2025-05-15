import json


def looks_bad(a):
    try:
        print("Looks Bad")
        print("How are you" + a)
    except TypeError as err:
        print("something bad happened")
        print(err)
        # raise err
    finally:
        print(". . .. Good bye .. . .")

# looks_bad(22)

x = [5, 89, 9]
t = isinstance(x,(int, str, float))
p = isinstance(x, list)
print(t)
print(p)
for tt in x:
    print(tt)

y = {"something": "beautiful", "how": "are you"}
a = json.dumps(y, indent=4)
print(type(a))
print(a)

a = json.dumps(x, indent=4)
print(type(a))
print(a)