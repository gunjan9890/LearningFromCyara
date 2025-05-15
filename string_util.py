import math

s = "0123456789"
# print(s[::-1][1:])
# d = []
# for i in range(len(s)-1, -1, -1):
#     d.append(s[i])
#
# rev = "".join(d)
# print(rev)
# print(s[::-1])


# words = ["why", "are", "real", "refrigeration", "is", "not", "simplified", "and", "often", "misrepresented", "in", "the", "balcony"]
words = ["Science","is","what","we","understand","well","enough","to","explain","to","a","computer.","Art","is","everything","else","we","do"]
maxLength = 20
current_sentence = ""
result = []
i = 1
start_index = 0
end_index = 0

while i <= len(words):
    current_sentence = "-".join(words[start_index: i])
    if len(current_sentence) > maxLength:
        end_index = i - 1
        # find spaces
        sub_arr = words[start_index: end_index]
        current_sentence = "".join(sub_arr)
        # print(f"Current Sentence : [{' '.join(sub_arr)}]. Length without spaces: {len(current_sentence)}")
        total_words = len(sub_arr)-1   # -1 because you dont put space at the end of the last word
        if total_words > 0:
            padding = (maxLength - len(current_sentence))
            average_space = padding / total_words
            # print(f"Total Padding Required : {maxLength - len(current_sentence)}. Total Words : {total_words}. Average Space : {average_space}")

            for j in range(0, total_words):
                spc = math.ceil(average_space)
                sub_arr.insert(j*2+1, " "*spc)
                total_words -= 1
                if total_words == 0:
                    break
                padding -= spc
                average_space = padding / total_words

        else:
            sub_arr.insert(1, " "*(maxLength - len(current_sentence)))
        # print(sub_arr)
        result.append("".join(sub_arr))
        start_index = end_index
    if i == len(words):
        sub_arr = words[start_index:]
        spc = (maxLength - len(" ".join(sub_arr)))*" "
        result.append(" ".join(words[start_index:]) + spc )

    i += 1

for w in result:
    print(w+".")

# sub_arr = ["what", "the", "fuck", "is", "wrong"]
# sub_arr.insert(1, " "*5)
# print(sub_arr)
# sub_arr.insert(3, " "*2)
# print(sub_arr)
# sub_arr.insert(5, " "*3)
# print(sub_arr)
# sub_arr.insert(7, " "*3)
# print(sub_arr)