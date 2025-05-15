import math

items = [5, 10, 15, 20, 25]

all_combinations = [[]]

for item in items:
    # print(item)
    temp_list = []
    for combinations_so_far in all_combinations:
        temp_list.append(combinations_so_far + [item])
    all_combinations = all_combinations + temp_list

print(all_combinations)
# print(all_combinations[1:])
# print(len(all_combinations))

for i in range(0, 3, 2):
    print(i)

