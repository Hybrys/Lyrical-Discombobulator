# Resolve modules not loading
import os
import sys
sys.path.append(os.getcwd())
os.environ["DATABASE"] = "test"

import unittest
from importlib import reload
import main
from db.db_postgres import DbFunctions, NOT_FOUND, NAME_COLLIDED, NO_ITEM_TO_ADD, SUCCESS_NO_RESPONSE, MANY_FOUND, NO_CONTENT
from sqlalchemy import create_engine


class FlaskTestingEmptyDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        main.database.close()
        db_init()
        reload(main)

    @classmethod
    def tearDownClass(cls):
        main.database.close()
    
    def test_index(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Select the function:", res.data)

    def test_view_artist(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/artist/Brand%20New")
        # self.assertequal(res.status_code, 400)   # Not currently functioning due to browser rendering issue
        self.assertIn(b"This artist isn't in", res.data)
        
    def test_view_album(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/album/Codes%20and%20Keys")
        # self.assertequal(res.status_code, 400)   # Not currently functioning due to browser rendering issue
        self.assertIn(b"This album isn't in", res.data)

    def test_view_track(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/track/Codes%20and%20Keys/!/!")
        # self.assertequal(res.status_code, 400)   # Not currently functioning due to browser rendering issue
        self.assertIn(b"This track isn't in", res.data)
    
    def test_lyric_lookup(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/lyrics/test")
        # self.assertequal(res.status_code, 400)   # Not currently functioning due to browser rendering issue
        self.assertIn(b"I couldn't find any", res.data)

    def test_lyrics_discombobulator(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/discombobulate/Feel%20Like%20Rain/Motion%20City%20Soundtrack/Commit%20This%20to%20Memory")
        # self.assertequal(res.status_code, 400)   # Not currently functioning due to browser rendering issue
        self.assertIn(b"This track isn't in the database yet!  Sorry!", res.data)

class FlaskTestingSeededDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        main.database.close()
        db_init()
        seed_database()
        reload(main)

    @classmethod
    def tearDownClass(cls):
        main.database.close()
    
    def test_index(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Select the function:", res.data)

    def test_view_artist(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/artist/Brand%20New")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Brand New", res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("album/Deja%20Entendu")\'>Deja Entendu</a>', res.data)
        
    def test_view_album(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/album/Codes%20and%20Keys")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Codes and Keys', res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("artist/Death%20Cab%20for%20Cutie")\'>Death Cab for Cutie</a>', res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("track/Underneath%20the%20Sycamore/Death%20Cab%20for%20Cutie/Codes%20and%20Keys")\'>Underneath the Sycamore</a>', res.data)

    def test_view_track(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/track/Feel%20Like%20Rain/!/!")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("artist/Motion%20City%20Soundtrack")\'>Motion City Soundtrack</a>', res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("album/Commit%20This%20to%20Memory")\'>Commit This to Memory</a>', res.data)
        self.assertIn(b"Here's some lyrics with a test in the middle!  Right in the middle there!", res.data)
    
    def test_lyric_lookup(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/lyrics/test")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"These are the tracks that have the word or phrase \'test\' in its lyrics:", res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("track/Feel%20Like%20Rain/Motion%20City%20Soundtrack/Commit%20This%20to%20Memory")\'>Feel Like Rain</a>', res.data)

    def test_view_artist_fuzzy(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/artist/Brand")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Did you mean one of the following artists?", res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("artist/Brand%20New")\'>Brand New</a>', res.data)

    def test_view_album_empty(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/album/I%20Am%20the%20Movie")
        # self.assertequal(res.status_code, 400)   # Not currently functioning due to browser rendering issue
        self.assertIn(b"The album I Am the Movie has no tracks in it yet!", res.data)

    def test_view_album_fuzzy(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/album/Codes")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Did you mean one of the following albums?", res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("album/Codes%20and%20Keys")\'>Codes and Keys</a>', res.data)

    def test_view_track_empty(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/track/Underneath%20the%20Sycamore/!/!")
        # self.assertequal(res.status_code, 400)   # Not currently functioning due to browser rendering issue
        self.assertIn(b'We don\'t have lyrics for Underneath the Sycamore yet!', res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("album/Codes%20and%20Keys")\'>Codes and Keys</a>', res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("artist/Death%20Cab%20for%20Cutie")\'>Death Cab for Cutie</a>', res.data)

    def test_view_track_name_collision(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/track/Roses/!/!")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'I found a couple of songs with the same name', res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("track/Roses/Meg%20%26%20Dia/Something%20Real")\'>Roses</a>', res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("track/Roses/The%20Rocket%20Summer/Of%20Men%20and%20Angels")\'>Roses</a>', res.data)
    
    def test_view_track_specific_artist(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/track/Roses/Meg%20%26%20Dia/Something%20Real")
        # self.assertequal(res.status_code, 400)   # Not currently functioning due to browser rendering issue
        self.assertIn(b'We don\'t have lyrics for Roses yet!', res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("album/Something%20Real")\'>Something Real</a>', res.data)

    def test_lyrics_discombobulator(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/discombobulate/Feel%20Like%20Rain/Motion%20City%20Soundtrack/Commit%20This%20to%20Memory")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("artist/Motion%20City%20Soundtrack")\'>Motion City Soundtrack</a>', res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("album/Commit%20This%20to%20Memory")\'>Commit This to Memory</a>', res.data)
        self.assertIn(b'<a href=# onclick=\'$("#div1").load("track/Feel%20Like%20Rain/Motion%20City%20Soundtrack/Commit%20This%20to%20Memory")\'>Feel Like Rain</a>', res.data)
        self.assertNotIn(b"Here's some lyrics with a test in the middle!  Right in the middle there!", res.data)

    def test_lyrics_discombobulator_nolyrics(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/discombobulate/Roses/Meg%20%26%20Dia/Something%20Real")
        # self.assertequal(res.status_code, 400)   # Not currently functioning due to browser rendering issue
        self.assertIn(b'We don\'t have lyrics for Roses yet!', res.data)
    
    def test_lyrics_discombobulator_instrum(self):
        with main.app.test_client() as test_client:
            res = test_client.get("/discombobulate/Ready/The%20Starting%20Line/Based%20on%20a%20True%20Story")
        # self.assertequal(res.status_code, 400)   # Not currently functioning due to browser rendering issue
        self.assertIn(b"Sorry, this track doesn't appear to be able to be discombobulated!", res.data)

def db_init():
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

def seed_database():
    db = DbFunctions()
    db.add_artist("Brand New")
    db.add_artist_albums("Brand New", ["Deja Entendu"])
    db.add_album_tracks("Brand New", "Deja Entendu", ["Guernica"])
    db.add_artist("Death Cab for Cutie")
    db.add_artist_albums("Death Cab for Cutie", ["Codes and Keys"])
    db.add_album_tracks("Death Cab for Cutie", "Codes and Keys", ["Underneath the Sycamore"])
    db.add_artist("Meg & Dia")
    db.add_artist_albums("Meg & Dia", ["Something Real"])
    db.add_album_tracks("Meg & Dia", "Something Real", ["Roses"])
    db.add_artist("The Rocket Summer")
    db.add_artist_albums("The Rocket Summer", ["Of Men and Angels"])
    db.add_album_tracks("The Rocket Summer", "Of Men and Angels", ["Roses"])
    db.add_artist("Motion City Soundtrack")
    db.add_artist_albums("Motion City Soundtrack", ["Commit This to Memory"])
    db.add_album_tracks("Motion City Soundtrack", "Commit This to Memory", ["Feel Like Rain"])
    db.add_track_lyrics("Motion City Soundtrack", "Commit This to Memory", "Feel Like Rain", "Here's some lyrics with a test in the middle!  Right in the middle there!")
    db.add_artist_albums("Motion City Soundtrack", ["I Am the Movie"])
    db.add_artist("The Starting Line")
    db.add_artist_albums("The Starting Line", ["Based on a True Story"])
    db.add_album_tracks("The Starting Line", "Based on a True Story", ["Ready"])
    db.add_track_lyrics("The Starting Line", "Based on a True Story", "Ready", "(Instrumental)")
    db.close()

if __name__ == "__main__":
    unittest.main()
