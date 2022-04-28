import syllapy
import nltk
import nltk.corpus
import re
import random
import pickle

WORD_STORE = {}
SPEC_CHAR = r"[ ,.!@#$%^&*()_+=\-/\\'\":;?\[\]]"

with open('./nlp/word_store.pickle', 'rb') as file:
    WORD_STORE = pickle.load(file)

def discombob(lyrics: str):
    result_list = []
    lyric_result = ""

    word_list = lyric_split(lyrics)
    if word_list == False:
        return False
    
    syllable_list = syllable_counter(word_list)
    word_list = nltk.pos_tag(word_list)

    for i, count in enumerate(syllable_list):
        if count == "NEWLINE":
            result_list.append("\n")
            continue
        if count not in WORD_STORE or word_list[i][-1] == 'PRP':
            result_list.append(word_list[i][0])
        else:
            while True:
                num = random.randrange(0, len(WORD_STORE[count]))
                if WORD_STORE[count][num][1] == word_list[i][1]:
                    result_list.append(WORD_STORE[count][num][0])
                    break
                else:
                    continue

    for word in result_list:
        if word == "\n":
            lyric_result += word
        else:
            lyric_result += f'{word} '
    
    return lyric_result

def syllable_counter(word_list: list):
    syllable_list = []

    for word in word_list:
        if len(word) < 1:
            continue
        if word == "NEWLINE":
            syllable_list.append(word)
            continue
        if word[0] not in SPEC_CHAR:
            count = syllapy.count(word)
            if count != 0:
                syllable_list.append(count)

    return syllable_list

def lyric_split(lyrics: str):
    word_list = lyrics.replace("\n", " NEWLINE ")
    word_list = re.split(" |\n|,|-", word_list)
    word_list = [x for x in word_list if len(x) >= 1]

    if len(word_list) < 2:
        return False    # I need more than one word
        
    return word_list
