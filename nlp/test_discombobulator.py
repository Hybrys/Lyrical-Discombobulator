from discombobulator import syllable_counter
import unittest

class DiscombobTesting(unittest.TestCase):
    def test_syllable_oneword(self):
        result = syllable_counter("Testing")
        self.assertEqual(result, False)
    
    def test_syllable_empty(self):
        result = syllable_counter("")
        self.assertEqual(result, False)
    
    def test_syllable_nonword(self):
        result = syllable_counter("Test 1 2 3")
        self.assertEqual(result, [1, 0, 0, 0])

    def test_syllable_phrase(self):
        result = syllable_counter("Test one two three")
        self.assertEqual(result, [1, 1, 1, 1])

    def test_syllable_hyphen(self):
        result = syllable_counter("Test forty-three")
        self.assertEqual(result, [1, 2, 1])
    
    def test_syllable_newline(self):
        result = syllable_counter("""Test
New
Lines""")
        self.assertEqual(result, [1, 1, 1])

    # def test_syllable_reallyrics(self):


if __name__ == "__main__":
    unittest.main()
