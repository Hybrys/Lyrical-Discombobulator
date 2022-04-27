# Resolve sibling modules not loading
import os
import sys
sys.path.append(os.getcwd())

from nlp import discombob
import unittest
import pickle
import os

class SyllableTesting(unittest.TestCase):
    def test_syllable_oneword(self):
        result = discombob.syllable_counter(["Testing"])
        self.assertEqual(result, [1])
    
    def test_syllable_empty(self):
        result = discombob.syllable_counter([""])
        self.assertEqual(result, [])
    
    def test_syllable_nonword(self):
        result = discombob.syllable_counter(["Test", "1", "2", "3"])
        self.assertEqual(result, [1])

    def test_syllable_phrase(self):
        result = discombob.syllable_counter(["Test", "one", "two", "three"])
        self.assertEqual(result, [1, 1, 1, 1])

class LyricSplitTesting(unittest.TestCase):
    def test_lyricsplit_oneword(self):
        result = discombob.lyric_split("Testing")
        self.assertEqual(result, False)

    def test_lyricsplit_phrase(self):
        result = discombob.lyric_split("Test one two three")
        self.assertEqual(result, ["Test", "one", "two", "three"])

    def test_lyricsplit_hyphen(self):
        result = discombob.lyric_split("Test forty-three")
        self.assertEqual(result, ["Test", "forty", "three"])

    def test_lyricsplit_newline(self):
        result = discombob.lyric_split("""Testing
New
Lines""")
        self.assertEqual(result, ["Testing", "New", "Lines"])
    
    def test_lyricsplit_reallyrics(self):
        with open("./tests/mock/death_cab_lyrics.pickle", "rb") as file:
            test_lyrics = pickle.load(file)
        result = discombob.lyric_split(test_lyrics)
        self.assertEqual(result, ['You', 'may', 'tire', 'of', 'me', 'as', 'our', 'December', 'sun', 'is', 'setting', 'because', "I'm", 'not', 'who', 'I', 'used', 'to', 'be', 'No', 'longer', 'easy', 'on', 'the', 'eyes', 'but', 'these', 'wrinkles', 'masterfully', 'disguise', 'The', 'youthful', 'boy', 'below', 'who', 'turned', 'your', 'way', 'and', 'saw', 'Something', 'he', 'was', 'not', 'looking', 'for:', 'both', 'a', 'beginning', 'and', 'an', 'end', 'But', 'now', 'he', 'lives', 'inside', 'someone', 'he', 'does', 'not', 'recognize', 'When', 'he', 'catches', 'his', 'reflection', 'on', 'accident', 'On', 'the', 'back', 'of', 'a', 'motor', 'bike', 'With', 'your', 'arms', 'outstretched', 'trying', 'to', 'take', 'flight', 'Leaving', 'everything', 'behind', 'But', 'even', 'at', 'our', 'swiftest', 'speed', 'we', "couldn't", 'break', 'from', 'the', 'concrete', 'In', 'the', 'city', 'where', 'we', 'still', 'reside.', 'And', 'I', 'have', 'learned', 'that', 'even', 'landlocked', 'lovers', 'yearn', 'for', 'the', 'sea', 'like', 'navy', 'men', 'Cause', 'now', 'we', 'say', 'goodnight', 'from', 'our', 'own', 'separate', 'sides', 'Like', 'brothers', 'on', 'a', 'hotel', 'bed', 'Like', 'brothers', 'on', 'a', 'hotel', 'bed', 'Like', 'brothers', 'on', 'a', 'hotel', 'bed', 'Like', 'brothers', 'on', 'a', 'hotel', 'bed', 'You', 'may', 'tire', 'of', 'me', 'As', 'our', 'December', 'sun', 'is', 'setting', 'Because', "I'm", 'not', 'who', 'I', 'used', 'to', 'be'])

class DiscombobTesting(unittest.TestCase):
    def test_discombob(self):
        result = discombob.discombob("Testing some lyrics")
        self.assertNotEqual(result, ["Testing", "some", "lyrics"])
        self.assertEqual(len(result), 3)

    def test_discombob_reallyrics(self):
        with open("./tests/mock/death_cab_lyrics.pickle", "rb") as file:
            test_lyrics = pickle.load(file)
        result = discombob.discombob(test_lyrics)
        self.assertNotEqual(result, ['You', 'may', 'tire', 'of', 'me', 'as', 'our', 'December', 'sun', 'is', 'setting', 'because', "I'm", 'not', 'who', 'I', 'used', 'to', 'be', 'No', 'longer', 'easy', 'on', 'the', 'eyes', 'but', 'these', 'wrinkles', 'masterfully', 'disguise', 'The', 'youthful', 'boy', 'below', 'who', 'turned', 'your', 'way', 'and', 'saw', 'Something', 'he', 'was', 'not', 'looking', 'for:', 'both', 'a', 'beginning', 'and', 'an', 'end', 'But', 'now', 'he', 'lives', 'inside', 'someone', 'he', 'does', 'not', 'recognize', 'When', 'he', 'catches', 'his', 'reflection', 'on', 'accident', 'On', 'the', 'back', 'of', 'a', 'motor', 'bike', 'With', 'your', 'arms', 'outstretched', 'trying', 'to', 'take', 'flight', 'Leaving', 'everything', 'behind', 'But', 'even', 'at', 'our', 'swiftest', 'speed', 'we', "couldn't", 'break', 'from', 'the', 'concrete', 'In', 'the', 'city', 'where', 'we', 'still', 'reside.', 'And', 'I', 'have', 'learned', 'that', 'even', 'landlocked', 'lovers', 'yearn', 'for', 'the', 'sea', 'like', 'navy', 'men', 'Cause', 'now', 'we', 'say', 'goodnight', 'from', 'our', 'own', 'separate', 'sides', 'Like', 'brothers', 'on', 'a', 'hotel', 'bed', 'Like', 'brothers', 'on', 'a', 'hotel', 'bed', 'Like', 'brothers', 'on', 'a', 'hotel', 'bed', 'Like', 'brothers', 'on', 'a', 'hotel', 'bed', 'You', 'may', 'tire', 'of', 'me', 'As', 'our', 'December', 'sun', 'is', 'setting', 'Because', "I'm", 'not', 'who', 'I', 'used', 'to', 'be'])
        self.assertEqual(len(result), 174)


if __name__ == "__main__":
    unittest.main()
