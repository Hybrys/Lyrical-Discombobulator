# Resolve sibling modules not loading
import os
import sys
sys.path.append(os.getcwd())

from discombob import discombob
import unittest
import pickle
import os

class DiscombobTesting(unittest.TestCase):
    def test_discombob(self):
        result = discombob.discombob("Testing some lyrics")
        self.assertNotEqual(result, "Testing some lyrics")
        self.assertEqual(len(result.split()), 3)

    def test_discombob_oneword(self):
        result = discombob.discombob("Testing")
        self.assertEqual(result, False)

    def test_discombob_death_cab_lyrics(self):
        with open("./tests/mock/death_cab_lyrics.pickle", "rb") as file:
            test_lyrics = pickle.load(file)
        result = discombob.discombob(test_lyrics)
        self.assertNotEqual(result, test_lyrics)
        self.assertNotIn("NEWLINE", result)
        self.assertEqual(len(result.split()), 174)
    
    def test_discombob_brand_new_lyrics(self):
        with open("./tests/mock/brand_new_lyrics.pickle", "rb") as file:
            test_lyrics = pickle.load(file)
        result = discombob.discombob(test_lyrics)
        self.assertNotEqual(result, test_lyrics)
        self.assertNotIn("NEWLINE", result)
        self.assertEqual(len(result.split()), 511)

    def test_discombob_brand_new_lyrics_italics(self):
        with open("./tests/mock/brand_new_lyrics_italics.pickle", "rb") as file:
            test_lyrics = pickle.load(file)
        result = discombob.discombob(test_lyrics)
        self.assertNotEqual(result, test_lyrics)
        self.assertNotIn("NEWLINE", result)
        self.assertEqual(len(result.split()), 338)

if __name__ == "__main__":
    unittest.main()
