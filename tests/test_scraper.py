# Resolve modules not loading
import os
import sys

sys.path.append(os.getcwd())

import unittest
from importlib import reload
import pickle
from requests.models import Response
from unittest.mock import patch, mock_open, Mock
from sqlalchemy import create_engine
import scraper.scraper as scraper
scraper.dbcur.close()

BADSTATUSRESPONSE = Mock(spec=Response)
BADSTATUSRESPONSE.text = "Don't you mock me."
BADSTATUSRESPONSE.status_code = 218

NOTFOUNDRESPONSE = Mock(spec=Response)
NOTFOUNDRESPONSE.text = "I can't believe I'm being mocked!"
NOTFOUNDRESPONSE.status_code = 404

class ScraperTesting(unittest.TestCase):
    def setUp(self):
        scraper.dbcur.close()
        db_init()
        os.environ["DATABASE"] = "test"
        reload(scraper)

    def test_add_artists_empty(self):
        with patch('builtins.open', mock_open(read_data='{"artists": ["Mute Math", "Oasis"]}')) as filemock:
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                scraper.add_artists()
            self.assertIn("Successfully added Mute Math to the db.", logs.output[1])
            self.assertIn("Successfully added Oasis to the db.", logs.output[2])

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
        self.assertIn("Successfully added albums for Cartel", logs.output[2])

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
        with patch('scraper.scraper.requests.get', side_effect=[BADSTATUSRESPONSE, response]):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_artist_albums("Brand New")
            self.assertIn("Successfully returning Brand New albums from lists", logs.output[-1])
            self.assertEqual(result, ['Your Favorite Weapon', 'Deja Entendu', 'The Devil and God Are Raging Inside Me', 'Daisy', 'Science Fiction'])

    def test_parse_artist_albums_artistpath(self):
        with open("./tests/mock/motion_city_artist.pickle", 'rb') as file:
            response = pickle.load(file)
        with patch('scraper.scraper.requests.get', side_effect=[BADSTATUSRESPONSE, BADSTATUSRESPONSE, response]):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_artist_albums("Motion City Soundtrack")
            self.assertIn("Successfully returning Motion City Soundtrack albums from lists", logs.output[-1])
            self.assertEqual(result, ['I Am the Movie', 'Commit This to Memory', 'Even If It Kills Me', 'My Dinosaur Life', 'Go', 'Panic Stations'])

    def test_parse_artist_albums_title_first_header(self):
        with open("./tests/mock/rem_titled_artist_page.pickle", 'rb') as file:
            response = pickle.load(file)
        with patch('scraper.scraper.requests.get', return_value=response):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_artist_albums("R.E.M.")
            self.assertIn("Successfully returning R.E.M. albums from tables", logs.output[-1])
            self.assertEqual(result, ['Murmur', 'Reckoning', 'Fables of the Reconstruction', 'Lifes Rich Pageant', 'Document', 'Green', 'Out of Time', 'Automatic for the People', 'Monster', 'New Adventures in Hi-Fi', 'Up', 'Reveal', 'Around the Sun', 'Accelerate', 'Collapse into Now'])

    @patch('scraper.scraper.requests.get', return_value=BADSTATUSRESPONSE)
    def test_parse_artist_albums_badstatus(self, mock):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            result = scraper.parse_artist_albums("Bad Status")
        self.assertIn("I'm 218ing please send help", logs.output[-3])
        self.assertEqual(result, [])

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
    
    @patch('scraper.scraper.dbcur.view_unparsed_albums', return_value=[["Mock", "Mock"]])
    @patch('scraper.scraper.parse_album_tracks', return_value=[])
    @patch('scraper.scraper.dbcur.add_album_tracks', return_value=scraper.SUCCESS_NO_RESPONSE)
    def test_get_tracks_fromdb_success(self, mock1, mock2, mock3):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_tracks()
        self.assertIn("Mock successfully had its tracks added to the db.", logs.output[-1])

    @patch('scraper.scraper.dbcur.view_unparsed_albums', return_value=[["Mock", "Mock"]])
    @patch('scraper.scraper.parse_album_tracks', return_value=[])
    @patch('scraper.scraper.dbcur.add_album_tracks', return_value=scraper.NOT_FOUND)
    def test_get_tracks_fromdb_not_found(self, mock1, mock2, mock3):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_tracks()
        self.assertIn("The album Mock from artist Mock was not found while trying to add tracks to the database!", logs.output[-1])

    @patch('scraper.scraper.dbcur.view_unparsed_albums', return_value=[["Mock", "Mock"]])
    @patch('scraper.scraper.parse_album_tracks', return_value=[])
    @patch('scraper.scraper.dbcur.add_album_tracks', return_value=scraper.NO_ITEM_TO_ADD)
    def test_get_tracks_fromdb_no_item_to_add(self, mock1, mock2, mock3):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_tracks()
        self.assertIn("The album Mock from artist Mock has an empty list for its tracks.  Check Falsed 'isparsed' items in the database", logs.output[-1])
    
    @patch('scraper.scraper.parse_album_tracks', return_value=[])
    @patch('scraper.scraper.dbcur.add_album_tracks', return_value=scraper.SUCCESS_NO_RESPONSE)
    def test_get_tracks_arg_success(self, mock1, mock2):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_tracks("Mock", "Mock")
        self.assertIn("Mock successfully had its tracks added to the db.", logs.output[-1])

    @patch('scraper.scraper.parse_album_tracks', return_value=[])
    @patch('scraper.scraper.dbcur.add_album_tracks', return_value=scraper.NOT_FOUND)
    def test_get_tracks_arg_not_found(self, mock1, mock2):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_tracks("Mock", "Mock")
        self.assertIn("The album Mock from artist Mock was not found while trying to add tracks to the database!", logs.output[-1])

    @patch('scraper.scraper.parse_album_tracks', return_value=[])
    @patch('scraper.scraper.dbcur.add_album_tracks', return_value=scraper.NO_ITEM_TO_ADD)
    def test_get_tracks_arg_no_item_to_add(self, mock1, mock2):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_tracks("Mock", "Mock")
        self.assertIn("The album Mock from artist Mock has an empty list for its tracks.  Check Falsed 'isparsed' items in the database", logs.output[-1])

    def test_parse_album_tracks_table(self):
        with open("./tests/mock/brand_new_yfw_album_page.pickle", 'rb') as file:
            response = pickle.load(file)
        with patch('scraper.scraper.requests.get', return_value=response):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_album_tracks("Brand New", "Your Favorite Weapon")
        self.assertIn("Successfully returning tracks for Your Favorite Weapon from a table!", logs.output[-1])
        self.assertEqual(result, ['The Shower Scene', 'Jude Law and a Semester Abroad', 'Sudden Death in Carolina', 'Mix Tape', 'Failure by Design', 'Last Chance to Lose Your Keys', 'Logan to Government Center', 'The No Seatbelt Song', 'Seventy Times 7', 'Secondary', 'Magazines', 'Soco Amaretto Lime'])

    def test_parse_album_tracks_albumpage(self):
        with open("./tests/mock/death_cab_plans_album_page.pickle", 'rb') as file:
            response = pickle.load(file)
        with patch('scraper.scraper.requests.get', side_effect=[BADSTATUSRESPONSE, response]):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_album_tracks("Death Cab for Cutie", "Plans")
        self.assertIn("Successfully returning tracks for Plans from a table!", logs.output[-1])
        self.assertEqual(result, ['Marching Bands of Manhattan', 'Soul Meets Body', 'Summer Skin', 'Different Names for the Same Thing', 'I Will Follow You into the Dark', 'Your Heart Is an Empty Room', 'Someday You Will Be Loved', 'Crooked Teeth', 'What Sarah Said', 'Brothers on a Hotel Bed', 'Stable Song'])

    def test_parse_album_tracks_list(self):
        with open("./tests/mock/motion_city_go_artalbum_page.pickle", 'rb') as file:
            response = pickle.load(file)
        with patch('scraper.scraper.requests.get', side_effect=[BADSTATUSRESPONSE, BADSTATUSRESPONSE, response]):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_album_tracks("Motion City Soundtrack", "Go")
        self.assertIn("Successfully returning tracks for Go from a list!", logs.output[-1])
        self.assertEqual(result, ['Circuits and Wires', 'True Romance', 'Son of a Gun', 'Timelines', 'Everyone Will Die', 'The Coma Kid', 'Boxelder', 'The Worst Is Yet to Come', 'Bad Idea', 'Happy Anniversary', 'Floating Down the River'])

    @patch('scraper.scraper.find_track_list', return_value=None)
    @patch('scraper.scraper.requests.get', return_value=BADSTATUSRESPONSE)
    def test_parse_album_tracks_none(self, mock, mock2):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            result = scraper.parse_album_tracks("Empty", "Finder")
        self.assertIn("I still can't find a wiki page for Empty's album Finder", logs.output[-1])
        self.assertEqual(result, [])

    @patch('scraper.scraper.find_track_list', return_value="I'm some bad soup")
    @patch('scraper.scraper.requests.get', return_value=BADSTATUSRESPONSE)
    def test_parse_album_tracks_badstatus(self, mock, mock2):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            result = scraper.parse_album_tracks("Bad", "Status")
        self.assertIn("I'm 218ing please send help", logs.output[-2])
        self.assertEqual(result, [])

    @patch('scraper.scraper.find_album_page', return_value=AttributeError)
    def test_parse_album_tracks_attriberror(self, mock):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            result = scraper.parse_album_tracks("Bad", "Attributes")
        self.assertIn("Whelp, I broke trying to parse Bad's album titled Attributes", logs.output[-1])
        self.assertEqual(result, [])

    def test_parse_album_tracks_typeerror(self):
        with open("./tests/mock/dylan_bob_dylan_typeerror_page.pickle", 'rb') as file:
            response = pickle.load(file)
        with patch('scraper.scraper.requests.get', return_value=response):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_album_tracks("Bob Dylan", "Dylan")
        self.assertIn("I typeerrored out trying to parse the album Dylan from Bob Dylan", logs.output[-1])
        self.assertEqual(result, [])

    @patch.object(scraper.time, 'sleep')
    @patch('scraper.scraper.dbcur.view_unparsed_tracks', return_value=[["Mock_Artist", "Mock_Album", "Mock_Track"]])
    @patch('scraper.scraper.parse_songlyricsdotcom', return_value="")
    @patch('scraper.scraper.dbcur.add_track_lyrics', return_value=scraper.SUCCESS_NO_RESPONSE)
    def test_get_lyrics_fromdb_success(self, mock1, mock2, mock3, mock4):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_lyrics()
        self.assertIn("Successfully added Mock_Track's lyrics to the db.", logs.output[-1])

    @patch.object(scraper.time, 'sleep')
    @patch('scraper.scraper.dbcur.view_unparsed_tracks', return_value=[["Mock_Artist", "Mock_Album", "Mock_Track"]])
    @patch('scraper.scraper.parse_songlyricsdotcom', return_value=[])
    @patch('scraper.scraper.dbcur.add_track_lyrics', return_value=scraper.NOT_FOUND)
    def test_get_lyrics_fromdb_not_found(self, mock1, mock2, mock3, mock4):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_lyrics()
        self.assertIn("Either the track Mock_Track or the album Mock_Album from artist Mock_Artist was not found!", logs.output[-1])

    @patch.object(scraper.time, 'sleep')
    @patch('scraper.scraper.dbcur.view_unparsed_tracks', return_value=[["Mock_Artist", "Mock_Album", "Mock_Track"]])
    @patch('scraper.scraper.parse_songlyricsdotcom', return_value=[])
    @patch('scraper.scraper.dbcur.add_track_lyrics', return_value=scraper.NO_ITEM_TO_ADD)
    def test_get_lyrics_fromdb_no_item_to_add(self, mock1, mock2, mock3, mock4):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_lyrics()
        self.assertIn("The track Mock_Track on album Mock_Album from artist Mock_Artist has an empty string for its lyrics!", logs.output[-1])
    
    @patch.object(scraper.time, 'sleep')
    @patch('scraper.scraper.parse_songlyricsdotcom', return_value=[])
    @patch('scraper.scraper.dbcur.add_track_lyrics', return_value=scraper.SUCCESS_NO_RESPONSE)
    def test_get_lyrics_arg_success(self, mock1, mock2, mock3):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_lyrics("Mock_Artist", "Mock_Album", "Mock_Track")
        self.assertIn("Successfully added Mock_Track's lyrics to the db.", logs.output[-1])

    @patch.object(scraper.time, 'sleep')
    @patch('scraper.scraper.parse_songlyricsdotcom', return_value=[])
    @patch('scraper.scraper.dbcur.add_track_lyrics', return_value=scraper.NOT_FOUND)
    def test_get_lyrics_arg_not_found(self, mock1, mock2, mock3):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_lyrics("Mock_Artist", "Mock_Album", "Mock_Track")
        self.assertIn("Either the track Mock_Track or the album Mock_Album from artist Mock_Artist was not found!", logs.output[-1])

    @patch.object(scraper.time, 'sleep')
    @patch('scraper.scraper.parse_songlyricsdotcom', return_value=[])
    @patch('scraper.scraper.dbcur.add_track_lyrics', return_value=scraper.NO_ITEM_TO_ADD)
    def test_get_lyrics_arg_no_item_to_add(self, mock1, mock2, mock3):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_lyrics("Mock_Artist", "Mock_Album", "Mock_Track")
        self.assertIn("The track Mock_Track on album Mock_Album from artist Mock_Artist has an empty string for its lyrics!", logs.output[-1])

    @patch.object(scraper.time, 'sleep')
    @patch('scraper.scraper.parse_songlyricsdotcom', return_value=[])
    @patch('scraper.scraper.dbcur.add_track_lyrics', return_value=scraper.SUCCESS_NO_RESPONSE)
    def test_get_lyrics_listarg_success(self, mock1, mock2, mock3):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_lyrics("Mock_Artist", "Mock_Album", ["Mock_Track"])
        self.assertIn("Successfully added Mock_Track's lyrics to the db.", logs.output[-1])

    @patch.object(scraper.time, 'sleep')
    @patch('scraper.scraper.parse_songlyricsdotcom', return_value=[])
    @patch('scraper.scraper.dbcur.add_track_lyrics', return_value=scraper.NOT_FOUND)
    def test_get_lyrics_listarg_not_found(self, mock1, mock2, mock3):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_lyrics("Mock_Artist", "Mock_Album", ["Mock_Track"])
        self.assertIn("Either the track Mock_Track or the album Mock_Album from artist Mock_Artist was not found!", logs.output[-1])

    @patch.object(scraper.time, 'sleep')
    @patch('scraper.scraper.parse_songlyricsdotcom', return_value=[])
    @patch('scraper.scraper.dbcur.add_track_lyrics', return_value=scraper.NO_ITEM_TO_ADD)
    def test_get_lyrics_listarg_no_item_to_add(self, mock1, mock2, mock3):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.get_lyrics("Mock_Artist", "Mock_Album", ["Mock_Track"])
        self.assertIn("The track Mock_Track on album Mock_Album from artist Mock_Artist has an empty string for its lyrics!", logs.output[-1])

    def test_parse_azlyrics(self):
        with open("./tests/mock/death_cab_plans_azlyrics.pickle", 'rb') as file:
            response = pickle.load(file)
        with open("./tests/mock/death_cab_lyrics.pickle", "rb") as file:
            test_lyrics = pickle.load(file)
        with patch('scraper.scraper.requests.get', return_value=response):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_azlyrics("Death Cab for Cutie", "Brothers on a Hotel Bed")
        self.assertIn("Successfully returning lyrics from lyricsh div for Brothers on a Hotel Bed by Death Cab for Cutie", logs.output[-1])
        self.assertEqual(result, test_lyrics)

    @patch('scraper.scraper.requests.get', return_value=NOTFOUNDRESPONSE)
    def test_parse_azlyrics_notfound(self, mock):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            result = scraper.parse_azlyrics("Death Cab for Cutie", "A Lack of Color (Demo)")
        self.assertIn("Removing parens from A Lack of Color (Demo) to see if I can get a better match", logs.output[0])
        self.assertIn("I'm 404ing please send help", logs.output[-2])
        self.assertEqual(result, "")

    @patch('scraper.scraper.str', return_value="I'm some bad soup!")
    def test_parse_azlyrics_attriberror(self, mock):
        with open("./tests/mock/brand_new_yfw_songlyricsdotcom.pickle", 'rb') as file:
            response = pickle.load(file)
        with patch('scraper.scraper.requests.get', return_value=response):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_azlyrics("Death Cab for Cutie", "We Looked Like Giants")
        self.assertIn("Failed finding the lyricsh div for We Looked Like Giants by Death Cab for Cutie", logs.output[-1])
        self.assertEqual(result, "")

    def test_parse_azlyrics_instrumental(self):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            result = scraper.parse_azlyrics("Brand New", "Some Track (Instrumental)")
            self.assertIn("I think this track Some Track (Instrumental) from Brand New is an instrumental, so I'm just returning nothing now", logs.output[-1])
            self.assertEqual(result, "")

    def test_azlyrics_format_strings_a_feat(self):
        result_artist, result_track = scraper.azlyrics_format_strings("A Day to Remember", "Reentry featuring Mark Hoppus")
        self.assertEqual(result_artist, "daytoremember")
        self.assertEqual(result_track, "reentry")
    
    def test_azlyrics_format_strings_amp(self):
        result_artist, result_track = scraper.azlyrics_format_strings("Meg & Dia", "Master & Commander")
        self.assertEqual(result_artist, "megdia")
        self.assertEqual(result_track, "masterandcommander")

    def test_azlyrics_format_strings_the(self):
        result_artist, result_track = scraper.azlyrics_format_strings("The Academy Is...", "Classifieds")
        self.assertEqual(result_artist, "academyis")
        self.assertEqual(result_track, "classifieds")

    def test_parse_songlyricsdotcom(self):
        with open("./tests/mock/brand_new_yfw_songlyricsdotcom.pickle", 'rb') as file:
            response = pickle.load(file)
        with open("./tests/mock/brand_new_lyrics.pickle", "rb") as file:
            test_lyrics = pickle.load(file)
        with patch('scraper.scraper.requests.get', return_value=response):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_songlyricsdotcom("Brand New", "Failure by Design")
        self.assertIn("Successfully returning lyrics from songLyricsDiv div for Failure by Design by Brand New", logs.output[-1])
        self.assertEqual(result, test_lyrics)

    @patch('scraper.scraper.requests.get', return_value=NOTFOUNDRESPONSE)
    def test_parse_songlyricsdotcom_notfound(self, mock):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            result = scraper.parse_songlyricsdotcom("Brand New", "Sowing Season (Yeah)")
        self.assertIn("Removing parens from Sowing Season (Yeah) to see if I can get a better match", logs.output[0])
        self.assertIn("I'm 404ing please send help", logs.output[-2])
        self.assertEqual(result, "")

    @patch('scraper.scraper.str', return_value="We do not have the lyrics for this song")
    def test_parse_songlyricsdotcom_nolyrics(self, mock):
        with open("./tests/mock/brand_new_yfw_songlyricsdotcom.pickle", 'rb') as file:
            response = pickle.load(file)
        with patch('scraper.scraper.requests.get', return_value=response):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_songlyricsdotcom("Brand New", "Seventy Times 7")
        self.assertIn("Songlyrics doesn't have the lyrics for Seventy Times 7 by Brand New", logs.output[-1])
        self.assertEqual(result, "")
    
    @patch('scraper.scraper.str', side_effect=AttributeError)
    def test_parse_songlyricsdotcom_attriberror(self, mock):
        with open("./tests/mock/brand_new_yfw_songlyricsdotcom.pickle", 'rb') as file:
            response = pickle.load(file)
        with patch('scraper.scraper.requests.get', return_value=response):
            with self.assertLogs('scraper_logger', level='DEBUG') as logs:
                result = scraper.parse_songlyricsdotcom("Brand New", "Jude Law and a Semester Abroad")
        self.assertIn("Failed finding the songLyricsDiv div for Jude Law and a Semester Abroad by Brand New", logs.output[-1])
        self.assertEqual(result, "")

    @patch('scraper.scraper.requests.get', side_effect=scraper.requests.exceptions.TooManyRedirects)
    def test_parse_songlyricsdotcom_redirectloop(self, mock):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            result = scraper.parse_songlyricsdotcom("Brand New", "Logan to Government Center")
            self.assertIn("Requests got stuck in a redirect loop with songlyrics.com while parsing Logan to Government Center from Brand New", logs.output[-1])
            self.assertEqual(result, "")

    def test_parse_songlyricsdotcom_instrumental(self):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            result = scraper.parse_songlyricsdotcom("Brand New", "Some Track (Instrumental)")
            self.assertIn("I think this track Some Track (Instrumental) from Brand New is an instrumental, so I'm just returning nothing now", logs.output[-1])
            self.assertEqual(result, "")

    def test_songlyricsdotcom_format_strings_a_feat(self):
        result_artist, result_track = scraper.songlyricsdotcom_format_strings("A Day to Remember", "Reentry featuring Mark Hoppus")
        self.assertEqual(result_artist, "day-to-remember")
        self.assertEqual(result_track, "reentry")
    
    def test_songlyricsdotcom_format_strings_mutemath(self):
        result_artist, result_track = scraper.songlyricsdotcom_format_strings("Mute Math", "Reset")
        self.assertEqual(result_artist, "mutemath")
        self.assertEqual(result_track, "reset")

    def test_songlyricsdotcom_format_strings_the(self):
        result_artist, result_track = scraper.songlyricsdotcom_format_strings("The Academy Is...", "Classifieds")
        self.assertEqual(result_artist, "academy-is")
        self.assertEqual(result_track, "classifieds")

    def test_songlyricsdotcom_format_strings_doublehyphen(self):
        result_artist, result_track = scraper.songlyricsdotcom_format_strings("Said  The Whale", "Honey  Lungs")
        self.assertEqual(result_artist, "said-the-whale")
        self.assertEqual(result_track, "honey-lungs")

    @patch.object(scraper.time, 'sleep')
    @patch('scraper.scraper.dbcur.second_pass_empty_tracks', return_value=[["Mock_Artist", "Mock_Album", "Mock_Track"]])
    @patch('scraper.scraper.parse_songlyricsdotcom', return_value=[])
    @patch('scraper.scraper.dbcur.add_track_lyrics', return_value=scraper.SUCCESS_NO_RESPONSE)
    def test_second_pass_lyrics(self, mock1, mock2, mock3, mock4):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.second_pass_lyrics()
        self.assertIn("Successfully added Mock_Track's lyrics to the db.", logs.output[-1])

    @patch.object(scraper.time, 'sleep')
    @patch('scraper.scraper.dbcur.second_pass_empty_tracks', return_value=[["Mock_Artist", "Mock_Album", "Mock_Track"]])
    @patch('scraper.scraper.parse_azlyrics', return_value=[])
    @patch('scraper.scraper.dbcur.add_track_lyrics', return_value=scraper.NOT_FOUND)
    def test_second_pass_lyrics_not_found(self, mock1, mock2, mock3, mock4):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.second_pass_lyrics()
        self.assertIn("Either the track Mock_Track or the album Mock_Album from artist Mock_Artist was not found!", logs.output[-1])

    @patch.object(scraper.time, 'sleep')
    @patch('scraper.scraper.dbcur.second_pass_empty_tracks', return_value=[["Mock_Artist", "Mock_Album", "Mock_Track"]])
    @patch('scraper.scraper.parse_azlyrics', return_value=[])
    @patch('scraper.scraper.dbcur.add_track_lyrics', return_value=scraper.NO_ITEM_TO_ADD)
    def test_second_pass_lyrics_no_item_to_add(self, mock1, mock2, mock3, mock4):
        with self.assertLogs('scraper_logger', level='DEBUG') as logs:
            scraper.second_pass_lyrics()
        self.assertIn("The track Mock_Track on album Mock_Album from artist Mock_Artist has an empty string for its lyrics!", logs.output[-1])

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
