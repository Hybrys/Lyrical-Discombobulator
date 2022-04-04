from db_postgres import *
from sqlalchemy import create_engine
import unittest

class DBTesting(unittest.TestCase):
    def setUp(self):
        setup_test_db()
        self.db = DbFunctions(db="test")
    
    def tearDown(self):
        self.db.close()

    def test_tests(self):
        print("Hello wurld!")

    def test_add_artist(self):
        resp = self.db.add_artist("Brand New")
        self.assertEqual(resp, SUCCESS_NO_RESPONSE)

    def test_view_artist(self):
        resp = self.db.view_artist_albums("Brand New")
        print(resp)
        self.assertEqual(resp, NOT_FOUND)

    
    # def test_add_album(self):
    #     resp = self.db.view_artist_albums("")

def setup_test_db():
    database = create_engine(f"postgresql+pg8000://postgres:@localhost:5454/postgres")
    with database.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT").execute("DROP DATABASE IF EXISTS test")
        conn.execute("CREATE DATABASE test")
    database.dispose()


if __name__ == "__main__":
    unittest.main()