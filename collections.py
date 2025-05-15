import copy

ar1 = [ {"name": "John", "age": 25}, {"name": "Jane", "age": 30} ]
print(ar1)
ar2 = copy.copy(ar1)
ar2[0]["name"] = "Jack"
print(ar1)

ar3 = copy.deepcopy(ar1)
ar3[1]["name"] = "Jill"
print(ar1)