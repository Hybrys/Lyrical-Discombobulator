
# Resolve modules not loading
import os
import sys
sys.path.append(os.getcwd())

import unittest
from db.db_postgres import DbFunctions, NOT_FOUND, NAME_COLLIDED, NO_ITEM_TO_ADD, SUCCESS_NO_RESPONSE, MANY_FOUND, NO_CONTENT
from sqlalchemy import create_engine
import main


class DBTesting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        main.database.close()
        os.environ["DATABASE"] = "test"
        
    def setUp(self):
        setup_test_db()
        self.db = DbFunctions()
    
    def tearDown(self):
        self.db.close()

    def test_add_artist(self):
        resp = self.db.add_artist("Brand New")
        self.assertEqual(resp, SUCCESS_NO_RESPONSE)

        resp = self.db.add_artist("Brand New")
        self.assertEqual(resp, NAME_COLLIDED)
    
    def test_add_artist_albums(self):
        resp = self.db.add_artist_albums("Death Cab for Cutie", ["Codes and Keys"])
        self.assertEqual(resp, NOT_FOUND)

        resp = self.db.add_artist_albums("Death Cab for Cutie", [])
        self.assertEqual(resp, NO_ITEM_TO_ADD)

        self.db.add_artist("Death Cab for Cutie")
        resp = self.db.add_artist_albums("Death Cab for Cutie", ["Codes and Keys"])
        self.assertEqual(resp, SUCCESS_NO_RESPONSE)

    def test_add_album_tracks(self):
        resp = self.db.add_album_tracks("Death Cab for Cutie", "Codes and Keys", ["Underneath the Sycamore"])
        self.assertEqual(resp, NOT_FOUND)

        self.db.add_artist("Death Cab for Cutie")
        resp = self.db.add_album_tracks("Death Cab for Cutie", "Codes and Keys", ["Underneath the Sycamore"])
        self.assertEqual(resp, NOT_FOUND)

        resp = self.db.add_album_tracks("Death Cab for Cutie", "Codes and Keys", [])
        self.assertEqual(resp, NOT_FOUND)

        self.db.add_artist_albums("Death Cab for Cutie", ["Codes and Keys"])
        resp = self.db.add_album_tracks("Death Cab for Cutie", "Codes and Keys", ["Underneath the Sycamore"])
        self.assertEqual(resp, SUCCESS_NO_RESPONSE)


    def test_add_track_lyrics(self):
        resp = self.db.add_track_lyrics("Death Cab for Cutie", "Codes and Keys", "Underneath the Sycamore", "Lyrics here! Get your lyrics here!")
        self.assertEqual(resp, NOT_FOUND)

        self.db.add_artist("Death Cab for Cutie")
        resp = self.db.add_track_lyrics("Death Cab for Cutie", "Codes and Keys", "Underneath the Sycamore", "Lyrics here! Get your lyrics here!")
        self.assertEqual(resp, NOT_FOUND)

        self.db.add_artist_albums("Death Cab for Cutie", ["Codes and Keys"])
        resp = self.db.add_track_lyrics("Death Cab for Cutie", "Codes and Keys", "Underneath the Sycamore", "Lyrics here! Get your lyrics here!")
        self.assertEqual(resp, NOT_FOUND)

        resp = self.db.add_track_lyrics("Death Cab for Cutie", "Codes and Keys", "Underneath the Sycamore", "")
        self.assertEqual(resp, NOT_FOUND)

        self.db.add_album_tracks("Death Cab for Cutie", "Codes and Keys", ["Underneath the Sycamore"])
        resp = self.db.add_track_lyrics("Death Cab for Cutie", "Codes and Keys", "Underneath the Sycamore", "Lyrics here! Get your lyrics here!")
        self.assertEqual(resp, SUCCESS_NO_RESPONSE)

    def test_view_unparsed_artists(self):
        resp = self.db.view_unparsed_artists()
        self.assertEqual(resp, [])

        self.db.add_artist("Death Cab for Cutie")
        resp = self.db.view_unparsed_artists()
        self.assertEqual(resp, ["Death Cab for Cutie"])

        self.db.add_artist_albums("Death Cab for Cutie", ["Codes and Keys"])
        resp = self.db.view_unparsed_artists()
        self.assertEqual(resp, [])

    def test_view_unparsed_albums(self):
        resp = self.db.view_unparsed_albums()
        self.assertEqual(resp, [])

        self.db.add_artist("Death Cab for Cutie")
        resp = self.db.view_unparsed_albums()
        self.assertEqual(resp, [])

        self.db.add_artist_albums("Death Cab for Cutie", ["Codes and Keys"])
        resp = self.db.view_unparsed_albums()
        self.assertEqual(resp, [["Death Cab for Cutie", "Codes and Keys"]])

        self.db.add_album_tracks("Death Cab for Cutie", "Codes and Keys", ["Underneath the Sycamore"])
        resp = self.db.view_unparsed_albums()
        self.assertEqual(resp, [])

    def test_view_unparsed_tracks(self):
        resp = self.db.view_unparsed_tracks()
        self.assertEqual(resp, [])

        self.db.add_artist("Death Cab for Cutie")
        resp = self.db.view_unparsed_tracks()
        self.assertEqual(resp, [])

        self.db.add_artist_albums("Death Cab for Cutie", ["Codes and Keys"])
        resp = self.db.view_unparsed_tracks()
        self.assertEqual(resp, [])

        self.db.add_album_tracks("Death Cab for Cutie", "Codes and Keys", ["Underneath the Sycamore", "Codes and Keys"])
        resp = self.db.view_unparsed_tracks()
        self.assertEqual(resp, [["Death Cab for Cutie", "Codes and Keys", "Underneath the Sycamore"], ["Death Cab for Cutie", "Codes and Keys", "Codes and Keys"]])

        # Test for inputting actual lyrics
        self.db.add_track_lyrics("Death Cab for Cutie", "Codes and Keys", "Underneath the Sycamore", "Lyrics here!  Get your lyrics here!")
        resp = self.db.view_unparsed_tracks()
        self.assertEqual(resp, [["Death Cab for Cutie", "Codes and Keys", "Codes and Keys"]])

        # Test for empty lyrics - this is to test the functionality of the parse_tried flag
        self.db.add_track_lyrics("Death Cab for Cutie", "Codes and Keys", "Codes and Keys", "")
        resp = self.db.view_unparsed_tracks()
        self.assertEqual(resp, [])

    def test_second_pass_empty_tracks(self):
        resp = self.db.second_pass_empty_tracks()
        self.assertEqual(resp, [])

        self.db.add_artist("Death Cab for Cutie")
        resp = self.db.second_pass_empty_tracks()
        self.assertEqual(resp, [])

        self.db.add_artist_albums("Death Cab for Cutie", ["Codes and Keys"])
        resp = self.db.second_pass_empty_tracks()
        self.assertEqual(resp, [])

        self.db.add_album_tracks("Death Cab for Cutie", "Codes and Keys", ["Underneath the Sycamore", "Codes and Keys"])
        resp = self.db.second_pass_empty_tracks()
        self.assertEqual(resp, [])

        # Test for inputting actual lyrics
        self.db.add_track_lyrics("Death Cab for Cutie", "Codes and Keys", "Underneath the Sycamore", "Lyrics here!  Get your lyrics here!")
        resp = self.db.second_pass_empty_tracks()
        self.assertEqual(resp, [])

        # Test for empty lyrics - this is to test the functionality of the parse_tried flag
        self.db.add_track_lyrics("Death Cab for Cutie", "Codes and Keys", "Codes and Keys", "")
        resp = self.db.second_pass_empty_tracks()
        self.assertEqual(resp, [["Death Cab for Cutie", "Codes and Keys", "Codes and Keys"]])

    def test_view_artist_albums(self):
        resp = self.db.view_artist_albums("Motion City Soundtrack")
        self.assertEqual(resp, NOT_FOUND)

        self.db.add_artist("Motion City Soundtrack")
        resp = self.db.view_artist_albums("Motion City Soundtrack")
        self.assertEqual(resp, NO_CONTENT)

        self.db.add_artist_albums("Motion City Soundtrack", ["Commit This to Memory"])
        resp = self.db.view_artist_albums("Motion City Soundtrack")
        self.assertEqual(resp, [["Motion City Soundtrack", "Commit This to Memory"]])

        self.db.add_artist_albums("Motion City Soundtrack", ["I Am The Movie"])
        resp = self.db.view_artist_albums("Motion City Soundtrack")
        self.assertEqual(resp, [["Motion City Soundtrack", "Commit This to Memory"], ["Motion City Soundtrack", "I Am The Movie"]])

    def test_view_artist_fuzzy(self):
        resp = self.db.view_artist_albums_fuzzy("Motion City")
        self.assertEqual(resp, NOT_FOUND)

        self.db.add_artist("Motion City Soundtrack")
        resp = self.db.view_artist_albums_fuzzy("Motion City")
        self.assertEqual(resp, [["Motion City Soundtrack"]])
    
        resp = self.db.view_artist_albums_fuzzy("nothere")
        self.assertEqual(resp, NOT_FOUND)

    def test_view_album_tracks(self):
        resp = self.db.view_album_tracks("Commit This to Memory")
        self.assertEqual(resp, NOT_FOUND)

        self.db.add_artist("Motion City Soundtrack")
        self.db.add_artist_albums("Motion City Soundtrack", ["Commit This to Memory"])
        resp = self.db.view_album_tracks("Commit This to Memory")
        self.assertEqual(resp, NO_CONTENT)

        self.db.add_album_tracks("Motion City Soundtrack", "Commit This to Memory", ["Feel Like Rain"])
        resp = self.db.view_album_tracks("Commit This to Memory")
        self.assertEqual(resp, [["Motion City Soundtrack", "Commit This to Memory", "Feel Like Rain"]])

        self.db.add_album_tracks("Motion City Soundtrack", "Commit This to Memory", ["When You're Around"])
        resp = self.db.view_album_tracks("Commit This to Memory")
        self.assertEqual(resp, [["Motion City Soundtrack", "Commit This to Memory", "Feel Like Rain"], ["Motion City Soundtrack", "Commit This to Memory", "When You're Around"]])

    def test_view_album_tracks_fuzzy(self):
        resp = self.db.view_album_tracks_fuzzy("Commit")
        self.assertEqual(resp, NOT_FOUND)

        self.db.add_artist("Motion City Soundtrack")
        self.db.add_artist_albums("Motion City Soundtrack", ["Commit This to Memory"])
        resp = self.db.view_album_tracks_fuzzy("Commit")
        self.assertEqual(resp, [(1, "Motion City Soundtrack", "Commit This to Memory")])

    def test_view_track_lyrics(self):
        resp1, resp2 = self.db.view_track_lyrics("Roses", "!", "!")
        self.assertEqual(resp1, NOT_FOUND)
        self.assertEqual(resp2, None)

        self.db.add_artist("Meg & Dia")
        self.db.add_artist_albums("Meg & Dia", ["Something Real"])
        self.db.add_album_tracks("Meg & Dia", "Something Real", ["Roses"])
        resp1, resp2 = self.db.view_track_lyrics("Roses", "!", "!")
        self.assertEqual(resp1, SUCCESS_NO_RESPONSE)
        self.assertEqual(resp2, [("Roses", None, "Meg & Dia", "Something Real")])

        resp1, resp2 = self.db.view_track_lyrics("Roses", "The Rocket Summer", "Of Men and Angels")
        self.assertEqual(resp1, NOT_FOUND)
        self.assertEqual(resp2, None)

        self.db.add_artist("The Rocket Summer")
        self.db.add_artist_albums("The Rocket Summer", ["Of Men and Angels"])
        self.db.add_album_tracks("The Rocket Summer", "Of Men and Angels", ["Roses"])
        resp1, resp2 = self.db.view_track_lyrics("Roses", "!", "!")
        self.assertEqual(resp1, MANY_FOUND)
        self.assertEqual(resp2, [["Roses", "Meg & Dia", "Something Real"], ["Roses", "The Rocket Summer", "Of Men and Angels"]])
        
        resp1, resp2 = self.db.view_track_lyrics("Roses", "The Rocket Summer", "Of Men and Angels")
        self.assertEqual(resp1, SUCCESS_NO_RESPONSE)
        self.assertEqual(resp2, [("Roses", None, "The Rocket Summer", "Of Men and Angels")])

        resp1, resp2 = self.db.view_track_lyrics("Roses", "The Rocket Summer", "!")
        self.assertEqual(resp1, NOT_FOUND)
        self.assertEqual(resp2, None)

    def test_lyric_lookup(self):
        resp = self.db.lyric_lookup("test")
        self.assertEqual(resp, NOT_FOUND)

        self.db.add_artist("Motion City Soundtrack")
        self.db.add_artist_albums("Motion City Soundtrack", ["Commit This to Memory"])
        self.db.add_album_tracks("Motion City Soundtrack", "Commit This to Memory", ["Feel Like Rain"])
        self.db.add_track_lyrics("Motion City Soundtrack", "Commit This to Memory", "Feel Like Rain", "Here's some lyrics with a test in the middle!  Right in the middle there!")
        resp = self.db.lyric_lookup("test")
        self.assertEqual(resp, [("Motion City Soundtrack", "Commit This to Memory", "Feel Like Rain")])

def setup_test_db():
    # Find out if I'm containerized
    container_check = os.environ.get('CONTAINER_DB')
    if container_check:
        database = create_engine(f"postgresql+pg8000://postgres:@pg:5454/postgres")
    else:
        database = create_engine(f"postgresql+pg8000://postgres:@localhost:5454/postgres")
    with database.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT").execute("DROP DATABASE IF EXISTS test")
        conn.execute("CREATE DATABASE test")
    database.dispose()

if __name__ == "__main__":
    unittest.main()
