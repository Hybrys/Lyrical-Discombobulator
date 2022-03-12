"""
Simple Artist/Album/Track/Lyric web scraper utilizing BeautifulSoup to parse Wikipedia, AZLyrics, and Songlyrics.com

Current hit rate as of March 11, 2022

899/1083 artists have albums (~83%)
6577/9674 albums have tracks (~68%)
45884/64375 tracks have lyrics (~71%)
"""


"""
TODO:
1. Resolve accenting - websites simply drop the accents rather than accepting URI encoded characters
2. Resolve TypeErroring in parse_tracks - this should be raising AttributeErrors if the object doesn't exist, so some conditional type conversion may need to take place to resolve this
3. Implement unittesting functionality
4. Create handler for parsing only artists that have no albums and albums that have no tracks - use LEFT JOIN on IDs where album_title and track_title IS NULL
5. Move from html.parser to LXML for ~25% speedup
6. Backtracking refactor (page by page stepping)
7. Consider edge-case handling by headless chrome instance (Playwright)
"""




from bs4 import BeautifulSoup
import re
import requests
import db
import json
import logging
import time
def parse_album(artist):
    """
    Parse the current artist, looking for their albums at a variety of Wikipedia addresses

    :param artist: The current artist to find their albums, as a string
    :return: Returns the albums as a list
    """
    albums = []
    artist = artist.replace(" ", "_")

    response = requests.get(f"https://en.wikipedia.org/wiki/{artist}_discography")
    soup = BeautifulSoup(response.text, 'html.parser')
    finder = find_album_list(soup)

    if finder == None:
        logging.debug(f"Discog checked, trying {artist}_(band)")
        response = requests.get(f"https://en.wikipedia.org/wiki/{artist}_(band)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_album_list(soup)

    if finder == None:
        logging.debug(f"Track listing wasn't found!  Trying just {artist}")
        response = requests.get(f"https://en.wikipedia.org/wiki/{artist}")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_album_list(soup)

    if response.status_code != 200:
        logging.critical(f"I'm {response.status_code}ing please send help")
        logging.critical(f"The artist is: {artist}")

    else:
        try:
            tabler = finder.parent.find_next_sibling("table")
            first_col = tabler.tbody.tr.th.text.rstrip().lower()

            if first_col == "year":
                for element in tabler.tbody.find_all("td"):
                    if element != None and element.i != None:
                        albums.append(element.i.text)

            elif first_col == "title":
                for element in tabler.tbody.find_all("tr"):
                    if element.th != None and element.th.i != None:
                        albums.append(element.th.i.text)

            logging.info(f"Successfully returning {artist} albums from tables")
            return albums

        except AttributeError:
            logging.debug(f"Failed to retrieve {artist}s albums from a table, trying a list")
            pass

        try:
            lister = finder.parent.find_next_sibling("ul")
            logging.debug(lister)
            if lister != None:
                for element in lister:
                    if element.name != None:
                        albums.append(element.i.text)
                logging.info(f"Successfully returning {artist} albums from lists")
            return albums
        except AttributeError:
            logging.error(f"I failed parsing any albums for {artist}")
            return albums


def parse_tracks(artist, album):
    """
    Parses the chosen album by one specific artist, using Wikipedia, looking for a list of the tracks

    :param artist: Name of the artist that the album belongs to as a string
    :param album: Title of the album as a string
    :return: Returns the tracks on an album as a list
    """

    tracks = []
    artist = artist.replace(" ", "_")
    album = album.replace(" ", "_")

    response = requests.get(f"https://en.wikipedia.org/wiki/{album}")
    soup = BeautifulSoup(response.text, 'html.parser')
    finder = find_track_list(soup)

    if finder == None:
        logging.debug(f"Track listing wasn't found!  Trying (album) for {album}")
        response = requests.get(f"https://en.wikipedia.org/wiki/{album}_(album)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_track_list(soup)

    if finder == None:
        logging.debug(f"Track listing wasn't found!  Trying ({artist}_album) for {album}")
        response = requests.get(f"https://en.wikipedia.org/wiki/{album}_({artist}_album)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_track_list(soup)

    if finder == None:
        logging.error(f"I still can't find a wiki page for {artist}'s album {album}")
        return tracks

    if response.status_code != 200:
        logging.critical(f"I'm {response.status_code}ing please send help")
        logging.critical(f"The artist is: {artist}\nThe album is: {album}")
        return tracks

    else:
        try:
            tabler = finder.parent.find_next_sibling("table")
            if tabler.tbody.tr.th != None:
                first_col = tabler.tbody.tr.th.text.rstrip().lower()
                if first_col == "no.":
                    for element in tabler.tbody("tr"):
                        if element.td != None and element.td.find_next_sibling("td") != None:
                            title_string = element.td.text
                            if title_string != None and title_string != "":
                                if title_string[0] == '"':
                                    title_string = title_string[1:title_string.find('"', 1)+1]
                                tracks.append(element.td.text.replace('"', ''))

                elif first_col == "title":
                    for element in tabler.tbody("tr"):
                        if element.td != None and element.td.find_previous_sibling("th") != None:
                            tracks.append(element.td.find_previous_sibling("th").i.text)
            logging.info(f"Successfully returning tracks for {album} from a table!")
            return tracks
        except AttributeError:
            pass

        try:
            lister = finder.parent.find_next_sibling("ol")
            logging.info(f"I didn't find a table for {album}, but I found an ordered list!")
            for element in lister("li"):
                hyphen = element.text.find("–")
                tracks.append((element.text[:hyphen-1].replace('"', '')))
            logging.info(f"Successfully returning tracks for {album} from a list!")
            return tracks
        except AttributeError:
            logging.error(f"Whelp, I broke trying to parse {artist}'s album titled {album}")
            return tracks
        except TypeError:
            logging.error(f"I typeerrored out trying to parse the album {album} from {artist}")
            return tracks


def parse_azlyrics(artist, track):
    """
    Parses the chosen track by one specific artist, using AZLyrics, looking for the lyrics in a specific div

    :param track: Title of the track as a string
    :param artist: Name of the artist that the album belongs to as a string
    :return: Returns the tracks on an album as a list
    """
    regex_spec_characters = r"[ ,.!@#$%^&*()_+=\-/\\'\":;?\[\]]"
    if "instrumental" in track:
        return ""

    no_space_artist = re.sub(regex_spec_characters, "", artist.lower())
    no_space_track = re.sub(regex_spec_characters, "", track.lower().replace("&", "and"))

    if artist[0:2].lower() == "a ":
        no_space_artist = re.sub(regex_spec_characters, "", artist[2:].lower())
    elif artist[0:4].lower() == "the ":
        no_space_artist = re.sub(regex_spec_characters, "", artist[3:].lower())

    featuring_filter = no_space_track.find("feat")
    if featuring_filter != -1:
        no_space_track = no_space_track[0:featuring_filter]

    response = requests.get(f"https://www.azlyrics.com/lyrics/{no_space_artist}/{no_space_track}.html")

    if response.status_code == 404:
        if "(" in track:
            parenindex = track.find("(")
            no_space_track = re.sub(regex_spec_characters, "", track[:parenindex].lower())
            response = requests.get(f"https://www.azlyrics.com/lyrics/{no_space_artist}/{no_space_track}.html")

    if response.status_code != 200:
        logging.critical(f"I'm {response.status_code}ing please send help")
        logging.critical(f"The artist is: {artist}\nThe track is: {track}")
        return ""
    else:
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            soup = soup.find(class_="lyricsh").find_next_sibling("b")
            div_string = str(soup.find_next_sibling("div"))
            comment_tag = div_string.find("-->")
            lyrics = div_string[comment_tag+3:].replace("</div>", "").replace("<br/>", "").replace("\r", "")
            return lyrics[1:-1]
        except AttributeError:
            logging.critical(f"Failed finding the lyricsh div for {track} by {artist}!")
            return ""


def parse_songlyricsdotcom(artist, track):
    """
    Parses the chosen track by one specific artist, using Songlyrics.com, looking for the lyrics in a specific div

    :param track: Title of the track as a string
    :param artist: Name of the artist that the album belongs to as a string
    :return: Returns the tracks on an album as a list
    """
    regex_spec_characters = r"[ ,.!@#$%^&*()_+=/\\'\":;?\[\]]"
    if "instrumental" in track:
        return ""

    no_space_artist = re.sub(regex_spec_characters, "", artist.replace(" ", "-").lower())
    no_space_track = re.sub(regex_spec_characters, "", track.replace(" ", "-").lower())

    if artist[0:2].lower() == "a ":
        no_space_artist = re.sub(regex_spec_characters, "", artist[2:].replace(" ", "-").lower())
    elif artist[0:4].lower() == "the ":
        no_space_artist = re.sub(regex_spec_characters, "", artist[3:].replace(" ", "-").lower())

    featuring_filter = no_space_track.find("feat")
    if featuring_filter != -1:
        no_space_track = no_space_track[0:featuring_filter]

    # special case handling
    if no_space_artist == "mute-math":
        no_space_artist = "mutemath"

    if no_space_artist[0] == "-":
        no_space_artist = no_space_artist[1:]

    if no_space_track != "":
        if no_space_track[-1] == "-":
            no_space_track = no_space_track[:-1]

    if "--" in no_space_artist:
        no_space_artist = no_space_artist.replace("--", "-")

    if "--" in no_space_track:
        no_space_track = no_space_track.replace("--", "-")

    try:
        response = requests.get(f"https://www.songlyrics.com/{no_space_artist}/{no_space_track}-lyrics/")
        if response.status_code == 404:
            if "(" in track:
                parenindex = track.find("(")
                no_space_track = re.sub(regex_spec_characters, "", track[:parenindex].replace(" ", "-").lower())
                no_space_track = no_space_track.replace("--", "-")
                if no_space_track != "":
                    if no_space_track[-1] == "-":
                        no_space_track = no_space_track[:-1]
                response = requests.get(f"https://www.songlyrics.com/{no_space_artist}/{no_space_track}-lyrics/")
    except requests.exceptions.TooManyRedirects:
        return ""

    if response.status_code != 200:
        logging.critical(f"I'm {response.status_code}ing please send help")
        logging.critical(f"The artist is: {artist}\nThe track is: {track}")
        return ""
    else:
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            lyrics = str(soup.find(id="songLyricsDiv").text)
            lyrics = lyrics.replace("(instrumental)", "").replace("[instrumental]", "").replace("[Instrumental]", "").replace("(Instrumental)", "")
            if "do not have the lyrics for" in lyrics:
                return ""
            else:
                return str(soup.find(id="songLyricsDiv").text)
        except AttributeError:
            logging.critical(f"Failed finding the lyricsh div for {track} by {artist}!")
            return ""


def find_album_list(soup):
    """
    Check the current BeautifulSoup object for relevant divs
    Helper function for 'parse_album{}'

    :param soup: BeautifulSoup object based on the current request response
    :return: Returns the correct div to start stepping from, or returns None in the case that all five divs are not found in the current BeautifulSoup object
    """
    finder = soup.find(id="Studio_albums")
    logging.debug(f"Album finder 1 {finder}")
    if finder != None:
        return finder
    finder = soup.find(id="Studio_album")
    logging.debug(f"Album finder 2 {finder}")
    if finder != None:
        return finder
    finder = soup.find(id="Studio,_live_and_soundtrack_albums")
    logging.debug(f"Album finder 3 {finder}")
    if finder != None:
        return finder
    finder = soup.find(id="Discography")
    logging.debug(f"Album finder 4 {finder}")
    if finder != None:
        return finder
    finder = soup.find(id="Albums")
    logging.debug(f"Album finder 5 {finder}")
    if finder != None:
        return finder
    logging.debug("helper failed out")
    return None


def find_track_list(soup):
    """
    Check the current BeautifulSoup object for relevant divs
    Helper function for 'parse_tracks{}'

    :param soup: BeautifulSoup object based on the current request response
    :return: Returns the correct div to start stepping from, or returns None in the case that all five divs are not found in the current BeautifulSoup object
    """
    finder = soup.find(id="Track_listing")
    logging.debug(f"Track finder 1 {finder}")
    if finder != None:
        return finder
    finder = soup.find(id="tracklist")
    logging.debug(f"Track finder 2 {finder}")
    if finder != None:
        return finder
    finder = soup.find(class_="tracklist")
    logging.debug(f"Track finder 3 {finder}")
    if finder != None:
        return finder
    return None


def add_artists(artists: list = []):
    """
    Attempts to add artists from a list to the database.  If the artist is already added, it will be rejected.

    :param artists: A list of artists to be added.  If defaulted to None, will open master_artist_list.json to use those names.
    """
    if artists == []:
        artistjson = open("master_artist_list.json")
        artistdata = json.load(artistjson)
        artists = artistdata["artists"]

    for artist in artists:
        resp = dbcur.add_artist(artist)
    if resp == db.NAME_COLLIDED:
        logging.debug(f"I collided with a name in the db for {artist}")
    else:
        logging.info(f"Successfully added {artist} to the db.")


def get_albums(artists: list = []):
    """
    Attempts to get an artists albums via the parse_album() function, then attempting to add those albums to the database.  Duplicates are rejected, but non-verbosely.

    :param artists: A list of artists whos albums should be retrieved.  If defaulted to None, it will check the database for artists that are not yet parsed according to the 'isparsed' flag.
    """
    if artists == []:
        artists = dbcur.view_unparsed_artists()

    for artist in artists:
        parsed_albums = parse_album(artist)
        resp = dbcur.add_artist_albums(artist, parsed_albums)
    if resp == db.NOT_FOUND:
        logging.critical(f"The album list for artist {artist[0]} were not found while trying to add tracks to the database!")
    else:
        logging.info(f"Successfully added albums for {artist[0]}")


def get_tracks(artist_name: str = "", album_title: str = ""):
    """
    Attempts to get an albums tracks via the parse_tracks() function, then attempting to add those tracks to the database.  Duplicates are rejected, but non-verbosely.

    :param artist_name: A string of the artist name whos album should be retrieved.  If defaulted to None, it will check the database for albums that have not yet been parsed via an 'isparsed' flag, and use element unpacking to assign artist_name to the first element of the response list.
    :param album_title: A string of the album name that should be retrieved.  If defaulted to None, it will check the database for albums that have not yet been parsed via an 'isparsed' flag, and use element unpacking to assign album_title to the second element of the response list.
    """

    # This logic should correctly refuse any instance where not all of the variables are defined
    if artist_name == "" or album_title == "":
        for artist_name, album_title in dbcur.view_unparsed_albums():
            parsed_albums = parse_tracks(artist_name, album_title)
            resp = dbcur.add_album_tracks(artist_name, album_title, parsed_albums)
            if resp == db.NOT_FOUND:
                logging.critical(f"The album {album_title} from artist {artist_name} were not found while trying to add tracks to the database!")
            elif resp == db.NO_ITEM_TO_ADD:
                logging.error(f"The album {album_title} from artist {artist_name} has an empty list for its tracks.  Check Falsed 'isparsed' items in the database")
            else:
                logging.info(f"Successfully added {album_title} had its tracks added to the db.")

    else:
        parsed_albums = parse_tracks(artist_name, album_title)
        resp = dbcur.add_album_tracks(artist_name, album_title, parsed_albums)
        if resp == db.NOT_FOUND:
            logging.critical(f"The album {album_title} from artist {artist_name} were not found while trying to add tracks to the database!")
        elif resp == db.NO_ITEM_TO_ADD:
            logging.error(f"The album {album_title} from artist {artist_name} has an empty list for its tracks.  Check Falsed 'isparsed' items in the database")
        else:
            logging.info(f"Successfully added {album_title} had its tracks added to the db.")


def get_lyrics(artist_name: str = "", album_title: str = "", track_title: str | list = ""):
    """
    Attempts to get a tracks lyrics, from the specified artist and album, via either the parse_azlyrics() or parse_songlyricsdotcom() function, then attempting to add those lyrics to the database.

    :param artist_name: A string of the artist name whos album should be retrieved.  If defaulted to None, it will check the database for tracks that have not had a parse attempted (via the 'parse_tried' flag), and use element unpacking to assign artist_name to the first element of the response list.
    :param album_title: A string of the album name that should be retrieved.  If defaulted to None, it will check the database for tracks that have not had a parse attempted (via the 'parse_tried' flag), and use element unpacking to assign album_title to the second element of the response list.
    :param track_title: A string or list of track titles that should have their lyrics retrieved.  If defaulted to None, it will check the database for tracks that have not had a parse attempted (via the 'parse_tried' flag), and use element unpacking to assign album_title to the third element of the response list.
    """
    multiplexing = 0

    # This logic should correctly refuse any instance where not all of the variables are defined
    if artist_name == "" or album_title == "" or track_title == "":
        for artist_name, album_title, track_title in dbcur.view_unparsed_tracks():
            multiplexing += 1
            if multiplexing % 2 == 0:
                parsed_tracks = parse_azlyrics(artist_name, track_title)
            else:
                parsed_tracks = parse_songlyricsdotcom(artist_name, track_title)
            resp = dbcur.add_track_lyrics(artist_name, album_title, track_title, parsed_tracks)
            if resp == db.NOT_FOUND:
                logging.critical(f"Either the track {track_title} or the album {album_title} from artist {artist_name} was not found!")
            elif resp == db.NO_ITEM_TO_ADD:
                logging.error(f"The track {track_title} on album {album_title} from artist {artist_name} has an empty string for its lyrics!  Check nulled 'lyrics' items in the database")
            else:
                logging.info(f"Successfully added {track_title}'s lyrics added to the db.")
            time.sleep(5)
    else:
        # Handling for track_title being a list of tracks from the same album/artist combination
        if type(track_title) != list:
            parsed_tracks = parse_azlyrics(artist_name, track_title)
            if parsed_tracks == "":
                parsed_tracks = parse_songlyricsdotcom(artist_name, track_title)
            resp = dbcur.add_track_lyrics(artist_name, album_title, track_title, parsed_tracks)
            if resp == db.NOT_FOUND:
                logging.critical(f"Either the track {track_title} or the album {album_title} from artist {artist_name} was not found!")
            elif resp == db.NO_ITEM_TO_ADD:
                logging.error(f"The track {track_title} on album {album_title} from artist {artist_name} has an empty string for its lyrics!  Check nulled 'lyrics' items in the database")
            else:
                logging.info(f"Successfully added {track_title}'s lyrics added to the db.")
        else:
            for track in track_title:
                multiplexing += 1
                if multiplexing % 2 == 0:
                    parsed_tracks = parse_azlyrics(artist_name, track_title)
                else:
                    parsed_tracks = parse_songlyricsdotcom(artist_name, track_title)
                resp = dbcur.add_track_lyrics(artist_name, album_title, track_title, parsed_tracks)
                if resp == db.NOT_FOUND:
                    logging.critical(f"Either the track {track_title} or the album {album_title} from artist {artist_name} was not found!")
                elif resp == db.NO_ITEM_TO_ADD:
                    logging.error(f"The track {track_title} on album {album_title} from artist {artist_name} has an empty string for its lyrics!  Check nulled 'lyrics' items in the database")
                else:
                    logging.info(f"Successfully added {track_title}'s lyrics added to the db.")
                time.sleep(5)


def second_pass_lyrics():
    """
    Attempts to get a tracks lyrics, from the specified artist and album, via either the parse_azlyrics() or parse_songlyricsdotcom() function, selected by commenting, then attempting to add those lyrics to the database.
    This function is meant for 'stubborn' tracks that may have been missed by one parser or the other, or to which needed additional scraper refinement before being properly picked up..

    This function takes no parameters and returns no information.
    """
    for artist_name, album_title, track_title, album_id in dbcur.second_pass_empty_tracks():
        parsed_tracks = parse_azlyrics(artist_name, track_title)
        # parsed_tracks = parse_songlyricsdotcom(artist_name, track_title)
        resp = dbcur.add_track_lyrics(artist_name, album_title, track_title, parsed_tracks)
        if resp == db.NOT_FOUND:
            logging.critical(f"Either the track {track_title} or the album {album_title} from artist {artist_name} was not found!")
        elif resp == db.NO_ITEM_TO_ADD:
            logging.error(f"The track {track_title} on album {album_title} from artist {artist_name} has an empty string for its lyrics!  Check nulled 'lyrics' items in the database")
        else:
            logging.info(f"Successfully added {track_title}'s lyrics added to the db.")
        time.sleep(10)


"""
Since this entire file is simply for database information population, these functions below are controlled based on commenting them in or out.

At the current stage of dataset refinement (March 11, 2022): 

I'm currently focusing on the largest dataset, the lyrics, and focusing efforting on improving the quality of that data.  Only second_pass_lyrics() is the intended function right now.
Log level remains on 'debug' to see verbose network traffic generated by Requests and diagnose larger issues.
"""

logging.basicConfig(level=logging.DEBUG)
dbcur = db.DbFunctions()

# add_artists()
# get_albums()
# get_tracks()
# get_lyrics()
second_pass_lyrics()
