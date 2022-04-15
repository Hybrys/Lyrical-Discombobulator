# Resolve modules not loading
import os
import sys

sys.path.append(os.getcwd())
os.environ["DATABASE"] = "test"

import unittest
from importlib import reload
import pickle
import scraper.scraper as scraper
from unittest.mock import patch, mock_open
from sqlalchemy import create_engine

class ScraperTesting(unittest.TestCase):
    def setUp(self):
        scraper.dbcur.close()
        db_init()
        reload(scraper)

    def test_add_artists_empty(self):
        with patch('builtins.open', mock_open(read_data='{"artists": ["Mute Math", "Oasis"]}')) as filemock:
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                scraper.add_artists()
            self.assertIn("Successfully added Mute Math to the db.", logs.output[0])
            self.assertIn("Successfully added Oasis to the db.", logs.output[1])

    def test_add_artists_list(self):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.add_artists(["Madeon"])
            scraper.add_artists(["Madeon"])
        self.assertIn("Successfully added Madeon to the db.", logs.output[0])
        self.assertIn("I collided with a name in the db for Madeon", logs.output[1])

    
    @patch('scraper.scraper.parse_artist_albums', return_value=['Cartel', 'Cycles'])
    def test_get_albums(self, mock):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.add_artists(["Cartel"])
            scraper.get_albums()
        self.assertIn("Successfully added Cartel to the db.", logs.output[0])
        self.assertIn("Successfully added albums for Cartel", logs.output[1])

    @patch('scraper.scraper.parse_artist_albums', return_value=['Cartel', 'Cycles'])
    def test_get_albums_not_found(self, mock):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_albums(["Cartel"])
        self.assertIn("The artist Cartel was not found while trying to add albums to the database!", logs.output[0])

    @patch('scraper.scraper.parse_artist_albums', return_value=[])
    def test_get_albums_no_items(self, mock):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_albums(["Cartel"])
        self.assertIn("The album list was empty for Cartel", logs.output[0])
        
    def test_parse_artist_albums_tables(self):
        with open("./tests/mock/death_cab_discog.pickle", 'rb') as file:
            response = pickle.load(file)
        with patch('scraper.scraper.requests.get', return_value=response):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_artist_albums("Death Cab for Cutie")
            self.assertIn("Successfully returning Death Cab for Cutie albums from tables", logs.output[-1])
            self.assertEqual(result, ['Something About Airplanes', "We Have the Facts and We're Voting Yes", 'The Photo Album', 'Transatlanticism', 'Plans', 'Narrow Stairs', 'Codes and Keys', 'Kintsugi', 'Thank You for Today'])

    def test_parse_artist_albums_lists(self):
        with open("./tests/mock/brand_new_band.pickle", 'rb') as file:
            response = pickle.load(file)
        with patch('scraper.scraper.requests.get', return_value=response):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_artist_albums("Brand New")
            self.assertIn("Successfully returning Brand New albums from lists", logs.output[-1])
            self.assertEqual(result, ['Your Favorite Weapon', 'Deja Entendu', 'The Devil and God Are Raging Inside Me', 'Daisy', 'Science Fiction'])

    @patch('scraper.scraper.find_artist_page', return_value=None)
    def test_parse_artist_albums_empty(self, mock):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            result = scraper.parse_artist_albums("Brand New")
        self.assertIn("Couldn't find an appropriate artist/discography page for Brand New!", logs.output[-1])
        self.assertEqual(result, [])

    @patch('scraper.scraper.find_artist_page', return_value="I'm some bad soup!")
    def test_parse_artist_albums_attribute_error(self, mock):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            result = scraper.parse_artist_albums("Brand New")
        self.assertIn("I failed parsing any albums for Brand New", logs.output[-1])
        self.assertEqual(result, [])

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

if __name__ == "__main__":
    unittest.main()
