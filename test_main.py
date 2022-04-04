from db_postgres import *
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class DBTesting(unittest.TestCase):
    def setUp(self):
        self.db = DbFunctions(db="test")
        print(self.db)
    
    def tearDown(self):
        DbFunctions.close()

    def test_tests(self):
        print("Hello wurld!")

    def test_add_artist(self):
        resp = self.db.add_artist("Brand New")
        self.assertEqual(resp, SUCCESS_NO_RESPONSE)

    def test_view_artist(self):
        resp = self.db.view_artist_albums("Brand New")
        self.assertEqual(resp, NOT_FOUND)

        self.db.add_artist
    
    def test_add_album(self):
        resp = self.db.view_artist_albums("")

def setup_test_db():
    pass

if __name__ == "__main__":
    unittest.main()