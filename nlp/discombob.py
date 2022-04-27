import cmudict
import syllapy
import re
import random

WORD_STORE = {}
SPEC_CHAR = r"[ ,.!@#$%^&*()_+=\-/\\'\":;?\[\]]"

for word in cmudict.dict():
    count = syllapy.count(word)
    if count not in WORD_STORE:
        WORD_STORE[count] = []
    WORD_STORE[count].append(word)


def discombob(lyrics: str):
    result_list = []

    word_list = lyric_split(lyrics)
    if word_list == False:
        return False

    syllable_list = syllable_counter(word_list)

    for i, count in enumerate(syllable_list):
        if count not in WORD_STORE:
            result_list.append(word_list[i])
        else:
            num = random.randrange(0, len(WORD_STORE[count]))
            result_list.append(WORD_STORE[count][num])
    
    return result_list


def syllable_counter(word_list: list):
    syllable_list = []

    for word in word_list:
        if len(word) < 1:
            continue
        if word[0] not in SPEC_CHAR:
            count = syllapy.count(word)
            if count != 0:
                syllable_list.append(count)

    return syllable_list

def lyric_split(lyrics: str):
    word_list = re.split(" |\n|,|-", lyrics)
    word_list = [x for x in word_list if len(x) >= 1]

    if len(word_list) < 2:
        return False    # I need more than one word
        
    return word_list
