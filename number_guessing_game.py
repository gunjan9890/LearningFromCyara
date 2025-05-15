from random import Random

num_lst = [1, 2, 3, 4, 5]
limit = 4
number = 0

for i in range(0, 5):
    r = Random().randint(0, limit)
    t = num_lst[r]
    num_lst.remove(t)
    number += (t*(10**limit))
    limit -= 1

# print(number)
flag = True
guess_count = 1
while flag:
    s = input(f"Enter your guess {guess_count} : ")
    if s == "stop":
        print(f"Number was [{number}]")
        break
    guess = int(s)
    if guess == number:
        print(f"BINGO. !! You Guessed it right in [{guess_count}] guesses")
        flag = False
    else:
        correct = 0
        for i in range(0, len(s)):
            correct += 1 if s[i] == str(number)[i] else 0
        print(f"No of Correct positions are : [{correct}]")

    guess_count += 1
