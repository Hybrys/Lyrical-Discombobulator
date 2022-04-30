import syllapy
import nltk
import nltk.corpus
import re
import random
import pickle

"""
Lyric 'Discombobulator'

This module 'remixes' lyrics, changing each possible word with another that is similar syllabically and is the same part of speech using NLTK and Syllapy
"""

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
    """
    Main function, taking the lyrics in and splitting them per line, passing each line into the 'discombob_line' private function

    :param lyrics: Lyrics passed in as a string.
    :return: Returns the remixed lyrics, maintaining formatting except for capitalization or,
             Returns False if the lyrics contain no whitespace between two non-whitespace characters
    """
    result_list = []

    line_list = re.split("\n", lyrics.lower())
    
    # This logic should refuse any single word 'lyrics', which often appears for 'instrumental' or 'incomprehensible' tracks
    if len(line_list) == 1:
        if len(lyrics.split()) < 2:
            return False

    for line in line_list:
        result_list.append(__discombob_line(line))
    
    return "".join(result_list)

def __discombob_line(line: str):
    """
    Helper function, which takes each line, tags it with part-of-speech information, then passes it to another function to do the randomization
    
    :param line: One line of lyrics as a string
    :returns: One line of remixed lyrics as a string
    """
    line_result = []

    if line == "":
        return "\n"

    if line[0] in SPEC_CHAR_LINE or line[-1] in SPEC_CHAR_LINE:
        return line.capitalize() + "\n"

    word_list = nltk.pos_tag(line.split())

    for word in word_list:
        line_result.append(__discombob_word(word))
    
    return " ".join(line_result).capitalize() + "\n"

def __discombob_word(word):
        """
        Helper function, which takes each word, measures the syllables, then replaces that word with one having the same syllable count and part of speech from the word store
        
        :param line: One word as a string
        :returns: One 'randomized' word as a string
        """
        failout = 0

        sylb_count = syllapy.count(word[0])

        # Directly return any proper nouns or special character wrapped words
        if sylb_count not in WORD_STORE or word[1] in ['NNP', 'NNPS', 'PRP']:
            return word[0].capitalize()
        elif word[0][-1] in SPEC_CHAR_WORD or word[0][0] in SPEC_CHAR_WORD:
            return word[0]
        else:
            # Endless loop prevention - This looks slow, but it's actually quite fast, with 10000 runs adding approx 0.01sec to runtime
            # TODO Make a map to resolve this 'guess and test' method
            while failout < 10000:  
                num = random.randrange(0, len(WORD_STORE[sylb_count]))
                if WORD_STORE[sylb_count][num][1] == word[1]:
                    return (WORD_STORE[sylb_count][num][0])
                failout += 1
            return word[0]
