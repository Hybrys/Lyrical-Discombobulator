import nltk
import nltk.corpus
import syllapy
import pickle
import re

SPEC_CHAR = r"[ ,.!@#$%^&*()_+=\-/\\'\":;?\[\]]"

word_store = {}

with open("./nlp/google-10000-handfilter.txt", "rt") as file:
    google_words = file.readlines()

google_set = set()

for word in google_words:
    google_set.add(word.replace("\n", "").lower())

for word in google_set:
    if word.title() not in nltk.corpus.names.words():
        count = syllapy.count(word)
        if not re.match(SPEC_CHAR, word):
            if count not in word_store:
                word_store[count] = []
            word_store[count].append(word)

for key in word_store.keys():
    word_store[key] = nltk.pos_tag(word_store[key])

with open('./nlp/word_store.pickle', 'wb') as file:
    pickle.dump(word_store, file)