import cmudict
import syllapy
import re

WORD_STORE = {}

for word in cmudict.dict():
    count = syllapy.count(word)
    if count not in WORD_STORE:
        WORD_STORE[count] = []
    WORD_STORE[count].append(word)

def syllable_counter(lyric: str):
    syllable_list = []
    word_list = re.split(" |\n|,|-", lyric)
    # print(word_list)
    if len(word_list) < 2:
        return False    # I need more than one word, dawg!
    for word in word_list:
        syllable_list.append(syllapy.count(word))
    return syllable_list

if __name__ == "__main__":
    print(syllable_counter(""))
