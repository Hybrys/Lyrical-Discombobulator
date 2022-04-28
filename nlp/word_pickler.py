import nltk
import nltk.corpus
import syllapy
import pickle

# This script does something

if __name__ == "__main__":
    # Downloads the corpus on first call, checks the version on subsequent calls
    nltk.download('names')
    word_store = {}

    with open("./nlp/google-10000-handfilter.txt", "rt") as file:
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

    with open('./nlp/word_store.pickle', 'wb') as file:
        pickle.dump(word_store, file)

else:
    print("Hey, you gotta run me manually!")