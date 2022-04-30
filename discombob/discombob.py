import syllapy
import nltk
import nltk.corpus
import re
import random
import pickle

WORD_STORE = {}
SPEC_CHAR_LINE = r"<>[@#$%^&*_+=\-/\\'\":;?\[\]0-9]"
SPEC_CHAR_WORD = r".,!<>[@#$%^&*()_+=\-/\\'\":;?\[\]0-9]"

# Downloads the tagger required if it cannot be found by NLTK
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

with open('./discombob/word_store.pickle', 'rb') as file:
    WORD_STORE = pickle.load(file)


def discombob(lyrics: str):
    result_list = []

    line_list = re.split("\n", lyrics.lower())
    
    if len(line_list) == 1:
        if len(lyrics.split()) < 2:
            return False

    for line in line_list:
        result_list.append(discombob_line(line))
    
    return "".join(result_list)

def discombob_line(line):
    line_result = []

    if line == "":
        return "\n"

    if line[0] in SPEC_CHAR_LINE or line[-1] in SPEC_CHAR_LINE:
        return line.capitalize() + "\n"

    word_list = nltk.pos_tag(line.split())

    for word in word_list:
        line_result.append(discombob_word(word))
    
    return " ".join(line_result).capitalize() + "\n"

def discombob_word(word):
        failout = 0

        sylb_count = syllapy.count(word[0])

        # Directly return any proper nouns or special character wrapped words
        if sylb_count not in WORD_STORE or word[1] in ['NNP', 'NNPS', 'PRP']:
            return word[0].capitalize()
        elif word[0][-1] in SPEC_CHAR_WORD or word[0][0] in SPEC_CHAR_WORD:
            return word[0]
        else:
            while failout < 10000:
                num = random.randrange(0, len(WORD_STORE[sylb_count]))
                if WORD_STORE[sylb_count][num][1] == word[1]:
                    return (WORD_STORE[sylb_count][num][0])
                failout += 1
            return word[0]
