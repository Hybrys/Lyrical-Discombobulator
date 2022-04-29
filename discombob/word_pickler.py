import nltk
import nltk.corpus
import syllapy
import pickle

# This script creates the word store with syllable counts using a hand-filtered version of Google's top 10000 words
# Word source: https://github.com/first20hours/google-10000-english

if __name__ == "__main__":

    # Downloads the corpus required if it cannot be found by NLTK
    try:
        nltk.data.find('corpora/names')
    except LookupError:
        nltk.download('names')
    
    word_store = {}

    with open("./discombob/google-10000-handfilter.txt", "rt") as file:
        google_words = file.readlines()

    google_set = set()

    for word in google_words:
        google_set.add(word.replace("\n", ""))

    for word in google_set:
        if word.title() not in nltk.corpus.names.words():
            count = syllapy.count(word)
            if count not in word_store:
                word_store[count] = []
            word_store[count].append(word)

    for key in word_store.keys():
        word_store[key] = nltk.pos_tag(word_store[key])

    with open('./discombob/word_store.pickle', 'wb') as file:
        pickle.dump(word_store, file)

else:
    print("Hey, you gotta run me manually!")