import syllapy
import nltk
import nltk.corpus
import re
import random
import pickle

WORD_STORE = {}
SPEC_CHAR = r"[ ,.!@#$%^&*()_+=\-/\\'\":;?\[\]]"

# Downloads the tagger required if it cannot be found by NLTK
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

with open('./discombob/word_store.pickle', 'rb') as file:
    WORD_STORE = pickle.load(file)

def discombob(lyrics: str):
    result_list = []
    lyric_result = ""

    word_list = lyric_split(lyrics.lower())
    # If the word-list only contains a single word, this may indicate that it is instrumental or incomprehensible
    if len(word_list) < 2:
        return False    
    
    syllable_list = syllable_counter(word_list)
    word_list = nltk.pos_tag(word_list)

    for i, sylb_count in enumerate(syllable_list):
        result_list.append(discombob_word(word_list[i], sylb_count))

    for word in result_list:
        if word == "\n":
            lyric_result += word
        else:
            lyric_result += f'{word} '
    
    return lyric_result

def discombob_word(word, sylb_count):
        failout = 0

        if sylb_count == "NEWLINE" or word[0] == "NEWLINE":
            return "\n"

        # Directly return any proper nouns
        elif sylb_count not in WORD_STORE or word[1] in ['NNP', 'NNPS'] or word[0][-1] in SPEC_CHAR:
            return word[0]
        else:
            while failout < 25:
                num = random.randrange(0, len(WORD_STORE[sylb_count]))
                if WORD_STORE[sylb_count][num][1] == word[1]:
                    return (WORD_STORE[sylb_count][num][0])
                failout += 1
            return word[0]
                

def syllable_counter(word_list: list):
    syllable_list = []

    for word in word_list:
        if len(word) < 1:
            continue
        if word == "NEWLINE":
            syllable_list.append(word)
            continue
        else:
            count = syllapy.count(word)
            if count > 0:
                syllable_list.append(count)

    return syllable_list

def lyric_split(lyrics: str):
    word_list = lyrics.replace("\n", " NEWLINE ")
    word_list = re.split(" |,|-", word_list)
    word_list = [x for x in word_list if len(x) >= 1]

    return word_list
