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

# Resolve modules not loading
import os
import sys
sys.path.append(os.getcwd())

from bs4 import BeautifulSoup
import re
import requests
from db.db_postgres import *
import json
import logging
import time

def add_artists(artists: list = []):
    """
    Attempts to add artists from a list to the database.  If the artist is already added, it will be rejected.

    :param artists: A list of artists to be added.  If defaulted to None, will open master_artist_list.json to use those names.
    """
    
    if artists == []:
        logger.info("I didn't find one or more required arguments.  Going into routine mode.")
        artistjson = open("./scraper/master_artist_list.json")
        artistdata = json.load(artistjson)
        artists = artistdata["artists"]

    for artist in artists:
        resp = dbcur.add_artist(artist)
        if resp == NAME_COLLIDED:
            logger.debug(f"I collided with a name in the db for {artist}")
        else:
            logger.info(f"Successfully added {artist} to the db.")


def get_albums(artists: list = []):
    """
    Attempts to get an artists albums via the parse_artist_album() function, then attempting to add those albums to the database.  Duplicates are rejected, but non-verbosely.

    :param artists: A list of artists whos albums should be retrieved.  If defaulted to None, it will check the database for artists that are not yet parsed according to the 'isparsed' flag.
    """

    if artists == []:
        logger.info("I didn't find one or more required arguments.  Going into routine mode.")
        artists = dbcur.view_unparsed_artists()

    if artists != []:
        for artist in artists:
            parsed_albums = parse_artist_albums(artist)
            resp = dbcur.add_artist_albums(artist, parsed_albums)
        if resp == NOT_FOUND:
            logger.critical(f"The artist {artist} was not found while trying to add albums to the database!")
        elif resp == NO_ITEM_TO_ADD:
            logger.critical(f"The album list was empty for {artist}")
        else:
            logger.info(f"Successfully added albums for {artist}")
    else:
        logger.info(f"No artists to parse!")

def parse_artist_albums(artist):
    """
    Parse the current artist, looking for their albums at a variety of Wikipedia addresses

    :param artist: The current artist to find their albums, as a string
    :return: Returns the albums as a list
    """

    albums = []
    
    finder = find_artist_page(artist)

    if finder == None:
        logger.debug(f"Couldn't find an appropriate artist/discography page for {artist}!")
        return albums   # Return empty list as failure result state

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

        logger.info(f"Successfully returning {artist} albums from tables")
        return albums

    except AttributeError:
        logger.debug(f"Failed to retrieve {artist}s albums from a table, trying a list")
        pass

    try:
        lister = finder.parent.find_next_sibling("ul")
        if lister != None:
            for element in lister:
                if element.name != None:
                    albums.append(element.i.text)
            logger.info(f"Successfully returning {artist} albums from lists")
        return albums
    except AttributeError:
        logger.error(f"I failed parsing any albums for {artist}")
        return albums   # Return empty list as failure result state

def find_artist_page(artist):
    """
    Helper function for parse_arist_albums() to step through possible pages on Wikipedia

    :param artist: The current artist to find their albums, as a string
    :returns finder: A BeautifulSoup object that has been stepped to the first instance of an 'album list' per find_album_list()
    """
    
    artist = artist.replace(" ", "_")

    response = requests.get(f"https://en.wikipedia.org/wiki/{artist}_discography")
    soup = BeautifulSoup(response.text, 'html.parser')
    finder = find_album_list_in_page(soup)

    if finder == None:
        logger.debug(f"Discog checked, trying {artist}_(band)")
        response = requests.get(f"https://en.wikipedia.org/wiki/{artist}_(band)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_album_list_in_page(soup)

    if finder == None:
        logger.debug(f"Track listing wasn't found!  Trying just {artist}")
        response = requests.get(f"https://en.wikipedia.org/wiki/{artist}")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_album_list_in_page(soup)

    if response.status_code != 200:
        logger.critical(f"I'm {response.status_code}ing please send help")
        logger.critical(f"The artist is: {artist}")
        return None
    
    else:
        return finder

def find_album_list_in_page(soup):
    """
    Check the current BeautifulSoup object for relevant divs
    Helper function for 'find_album_page{}'

    :param soup: BeautifulSoup object based on the current request response
    :return: Returns the correct div to start stepping from, or returns None in the case that all five divs are not found in the current BeautifulSoup object
    """

    finder = soup.find(id="Studio_albums")
    logger.debug(f"Album finder 1 {finder}")
    if finder != None:
        return finder
    finder = soup.find(id="Studio_album")
    logger.debug(f"Album finder 2 {finder}")
    if finder != None:
        return finder
    finder = soup.find(id="Studio,_live_and_soundtrack_albums")
    logger.debug(f"Album finder 3 {finder}")
    if finder != None:
        return finder
    finder = soup.find(id="Discography")
    logger.debug(f"Album finder 4 {finder}")
    if finder != None:
        return finder
    finder = soup.find(id="Albums")
    logger.debug(f"Album finder 5 {finder}")
    if finder != None:
        return finder
    logger.debug("Album list helper failed out")
    return None

def get_tracks(artist_name: str = "", album_title: str = ""):
    """
    Attempts to get an albums tracks via the parse_tracks() function, then attempting to add those tracks to the database.  Duplicates are rejected, but non-verbosely.

    :param artist_name: A string of the artist name whos album should be retrieved.  If defaulted to None, it will check the database for albums that have not yet been parsed via an 'isparsed' flag, and use element unpacking to assign artist_name to the first element of the response list.
    :param album_title: A string of the album name that should be retrieved.  If defaulted to None, it will check the database for albums that have not yet been parsed via an 'isparsed' flag, and use element unpacking to assign album_title to the second element of the response list.
    """

    # This logic should correctly refuse any instance where even one of the variables is left undefined
    # If this happens, it goes into routine mode where it looks up currently unparsed albums
    if artist_name == "" or album_title == "":
        logger.info("I didn't find one or more required arguments.  Going into routine mode.")
        for artist_name, album_title in dbcur.view_unparsed_albums():
            parsed_track_list = parse_album_tracks(artist_name, album_title)
            resp = dbcur.add_album_tracks(artist_name, album_title, parsed_track_list)
            if resp == NOT_FOUND:
                logger.critical(f"The album {album_title} from artist {artist_name} was not found while trying to add tracks to the database!")
            elif resp == NO_ITEM_TO_ADD:
                logger.error(f"The album {album_title} from artist {artist_name} has an empty list for its tracks.  Check Falsed 'isparsed' items in the database")
            else:
                logger.info(f"{album_title} successfully had its tracks added to the db.")

    else:
        parsed_track_list = parse_album_tracks(artist_name, album_title)
        resp = dbcur.add_album_tracks(artist_name, album_title, parsed_track_list)
        if resp == NOT_FOUND:
            logger.critical(f"The album {album_title} from artist {artist_name} was not found while trying to add tracks to the database!")
        elif resp == NO_ITEM_TO_ADD:
            logger.error(f"The album {album_title} from artist {artist_name} has an empty list for its tracks.  Check Falsed 'isparsed' items in the database")
        else:
            logger.info(f"{album_title} successfully had its tracks added to the db.")


def parse_album_tracks(artist, album):
    """
    Parses the chosen album by one specific artist, using Wikipedia, looking for a list of the tracks

    :param artist: Name of the artist that the album belongs to as a string
    :param album: Title of the album as a string
    :return: Returns the tracks on an album as a list
    """

    tracks = []

    finder = find_album_page(artist, album)
    
    if finder == None:
        return tracks   # Return empty list as failure result state

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
        if tracks == []:
            logger.info(f"I found a table, but I didn't get the tracks for {album} from it.")
            raise ValueError    # Raised error to advance the state if the track system is still empty and hasn't errored out yet
        logger.info(f"Successfully returning tracks for {album} from a table!")
        return tracks
    except (AttributeError, ValueError):
        pass    # Resolving expected errors to get them into the next Try block

    try:
        lister = finder.parent.find_next_sibling("ol")
        logger.info(f"I didn't find a table for {album} or didn't get a track list from it, but I found an ordered list!")
        for element in lister("li"):
            hyphen = element.text.find("–") # This is intentionally an odd hyphen (character U+2013) 
            tracks.append((element.text[:hyphen-1].replace('"', '')))
        logger.info(f"Successfully returning tracks for {album} from a list!")
        return tracks
    except AttributeError:
        logger.error(f"Whelp, I broke trying to parse {artist}'s album titled {album}")
        return tracks
    except TypeError:
        logger.error(f"I typeerrored out trying to parse the album {album} from {artist}")
        return tracks

def find_album_page(artist, album):
    """
    Helper function for parse_album_tracks() to step through possible pages on Wikipedia

    :param artist: Name of the artist that the album belongs to as a string
    :param album: Title of the album as a string
    :returns finder: A BeautifulSoup object that has been stepped to the first instance of a 'track list' per find_track_list()
    """

    artist = artist.replace(" ", "_")
    album = album.replace(" ", "_")

    response = requests.get(f"https://en.wikipedia.org/wiki/{album}")
    soup = BeautifulSoup(response.text, 'html.parser')
    finder = find_track_list(soup)

    if finder == None:
        logger.debug(f"Track listing wasn't found!  Trying (album) for {album}")
        response = requests.get(f"https://en.wikipedia.org/wiki/{album}_(album)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_track_list(soup)

    if finder == None:
        logger.debug(f"Track listing wasn't found!  Trying ({artist}_album) for {album}")
        response = requests.get(f"https://en.wikipedia.org/wiki/{album}_({artist}_album)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_track_list(soup)

    if finder == None:
        logger.error(f"I still can't find a wiki page for {artist}'s album {album}")
        return None

    if response.status_code != 200:
        logger.critical(f"I'm {response.status_code}ing please send help")
        logger.critical(f"The artist is: {artist}\nThe album is: {album}")
        return None

    else:
        return finder


def find_track_list(soup):
    """
    Check the current BeautifulSoup object for relevant divs
    Helper function for 'parse_tracks{}'

    :param soup: BeautifulSoup object based on the current request response
    :return: Returns the correct div to start stepping from, or returns None in the case that all five divs are not found in the current BeautifulSoup object
    """

    finder = soup.find(id="Track_listing")
    logger.debug(f"Track finder 1 {finder}")
    if finder != None:
        return finder
    finder = soup.find(id="tracklist")
    logger.debug(f"Track finder 2 {finder}")
    if finder != None:
        return finder
    finder = soup.find(class_="tracklist")
    logger.debug(f"Track finder 3 {finder}")
    if finder != None:
        return finder
    logger.debug("Track list helper failed out")
    return None

def get_lyrics(artist_name: str = "", album_title: str = "", track_title: str | list = ""):
    """
    Attempts to get a tracks lyrics, from the specified artist and album, via either the parse_azlyrics() or parse_songlyricsdotcom() function, then attempting to add those lyrics to the database.

    :param artist_name: A string of the artist name whos album should be retrieved.  If defaulted to None, it will check the database for tracks that have not had a parse attempted (via the 'parse_tried' flag), and use element unpacking to assign artist_name to the first element of the response list.
    :param album_title: A string of the album name that should be retrieved.  If defaulted to None, it will check the database for tracks that have not had a parse attempted (via the 'parse_tried' flag), and use element unpacking to assign album_title to the second element of the response list.
    :param track_title: A string or list of track titles that should have their lyrics retrieved.  If defaulted to None, it will check the database for tracks that have not had a parse attempted (via the 'parse_tried' flag), and use element unpacking to assign album_title to the third element of the response list.
    """
    
    multiplexing = 0

    # This logic should correctly capture any instance where not all of the variables are defined
    # If this happens, it goes into routine mode where it looks up currently unparsed tracks
    if artist_name == "" or album_title == "" or track_title == "":
        logger.info("I didn't find one or more required arguments.  Going into routine mode.")
        for artist_name, album_title, track_title in dbcur.view_unparsed_tracks():
            multiplexing += 1
            if multiplexing % 2 == 0:
                parsed_tracks = parse_azlyrics(artist_name, track_title)
            else:
                parsed_tracks = parse_songlyricsdotcom(artist_name, track_title)
            resp = dbcur.add_track_lyrics(artist_name, album_title, track_title, parsed_tracks)
            if resp == NOT_FOUND:
                logger.critical(f"Either the track {track_title} or the album {album_title} from artist {artist_name} was not found!")
            elif resp == NO_ITEM_TO_ADD:
                logger.error(f"The track {track_title} on album {album_title} from artist {artist_name} has an empty string for its lyrics!  Check nulled 'lyrics' items in the database")
            else:
                logger.info(f"Successfully added {track_title}'s lyrics to the db.")
            time.sleep(5)
    else:
        # Handling for track_title being a list of tracks from the same album/artist combination
        if type(track_title) != list:
            parsed_tracks = parse_azlyrics(artist_name, track_title)
            if parsed_tracks == "":
                parsed_tracks = parse_songlyricsdotcom(artist_name, track_title)
            resp = dbcur.add_track_lyrics(artist_name, album_title, track_title, parsed_tracks)
            if resp == NOT_FOUND:
                logger.critical(f"Either the track {track_title} or the album {album_title} from artist {artist_name} was not found!")
            elif resp == NO_ITEM_TO_ADD:
                logger.error(f"The track {track_title} on album {album_title} from artist {artist_name} has an empty string for its lyrics!  Check nulled 'lyrics' items in the database")
            else:
                logger.info(f"Successfully added {track_title}'s lyrics to the db.")
        else:
            for track in track_title:
                multiplexing += 1
                if multiplexing % 2 == 0:
                    parsed_tracks = parse_azlyrics(artist_name, track)
                else:
                    parsed_tracks = parse_songlyricsdotcom(artist_name, track)
                resp = dbcur.add_track_lyrics(artist_name, album_title, track, parsed_tracks)
                if resp == NOT_FOUND:
                    logger.critical(f"Either the track {track} or the album {album_title} from artist {artist_name} was not found!")
                elif resp == NO_ITEM_TO_ADD:
                    logger.error(f"The track {track} on album {album_title} from artist {artist_name} has an empty string for its lyrics!  Check nulled 'lyrics' items in the database")
                else:
                    logger.info(f"Successfully added {track}'s lyrics to the db.")
                time.sleep(5)

def azlyrics_format_strings(artist, track):
    regex_spec_characters = r"[ ,.!@#$%^&*()_+=\-/\\'\":;?\[\]]"

    no_space_artist = re.sub(regex_spec_characters, "", artist.lower())
    no_space_track = re.sub(regex_spec_characters, "", track.lower().replace("&", "and"))

    if artist[0:2].lower() == "a ":
        no_space_artist = re.sub(regex_spec_characters, "", artist[2:].lower())
    elif artist[0:4].lower() == "the ":
        no_space_artist = re.sub(regex_spec_characters, "", artist[3:].lower())

    featuring_filter = no_space_track.find("feat")
    if featuring_filter != -1:
        no_space_track = no_space_track[0:featuring_filter]

    return no_space_artist, no_space_track

def parse_azlyrics(artist, track):
    """
    Parses the chosen track by one specific artist, using AZLyrics, looking for the lyrics in a specific div

    :param track: Title of the track as a string
    :param artist: Name of the artist that the album belongs to as a string
    :return: Returns the tracks on an album as a list
    """
    regex_spec_characters = r"[ ,.!@#$%^&*()_+=\-/\\'\":;?\[\]]"

    if "instrumental" in track.lower():
        logger.debug(f"I think this track {track} from {artist} is an instrumental, so I'm just returning nothing now")
        return ""
    
    no_space_artist, no_space_track = azlyrics_format_strings(artist, track)

    response = requests.get(f"https://www.azlyrics.com/lyrics/{no_space_artist}/{no_space_track}.html")

    if response.status_code == 404:
        if "(" in track:
            parenindex = track.find("(")
            logger.info(f"Removing parens from {track} to see if I can get a better match")
            no_space_track = re.sub(regex_spec_characters, "", track[:parenindex].lower())
            response = requests.get(f"https://www.azlyrics.com/lyrics/{no_space_artist}/{no_space_track}.html")

    if response.status_code != 200:
        logger.critical(f"I'm {response.status_code}ing please send help")
        logger.critical(f"The artist is: {artist}\nThe track is: {track}")
        return ""

    else:
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            soup = soup.find(class_="lyricsh").find_next_sibling("b")
            div_string = str(soup.find_next_sibling("div"))
            comment_tag = div_string.find("-->")
            lyrics = div_string[comment_tag+3:].replace("</div>", "").replace("<br/>", "").replace("\r", "")
            logger.info(f"Successfully returning lyrics from lyricsh div for {track} by {artist}")
            return lyrics[1:-1]

        except AttributeError:
            logger.critical(f"Failed finding the lyricsh div for {track} by {artist}!")
            return ""

def parse_songlyricsdotcom(artist, track):
    """
    Parses the chosen track by one specific artist, using Songlyrics.com, looking for the lyrics in a specific div

    :param track: Title of the track as a string
    :param artist: Name of the artist that the album belongs to as a string
    :return: Returns the tracks on an album as a list
    """
    regex_spec_characters = r"[ ,.!@#$%^&*()_+=/\\'\":;?\[\]]"

    if "instrumental" in track.lower():
        logger.debug(f"I think this track {track} from {artist} is an instrumental, so I'm just returning nothing now")
        return ""

    no_space_artist, no_space_track = songlyricsdotcom_format_strings(artist, track)
    
    try:
        response = requests.get(f"https://www.songlyrics.com/{no_space_artist}/{no_space_track}-lyrics/")
        
        if response.status_code == 404:
            if "(" in track:
                logger.info(f"Removing parens from {track} to see if I can get a better match")
                parenindex = track.find("(")
                no_space_track = re.sub(regex_spec_characters, "", track[:parenindex].replace(" ", "-").lower())
                no_space_track = no_space_track.replace("--", "-")
                if no_space_track != "":
                    if no_space_track[-1] == "-":
                        no_space_track = no_space_track[:-1]
                response = requests.get(f"https://www.songlyrics.com/{no_space_artist}/{no_space_track}-lyrics/")

    except requests.exceptions.TooManyRedirects:    # Handles an edge case where the scraper was stuck in a redirect loop
        logger.debug(f"Requests got stuck in a redirect loop with songlyrics.com while parsing {track} from {artist}")
        return ""

    if response.status_code != 200:
        logger.critical(f"I'm {response.status_code}ing please send help")
        logger.critical(f"The artist is: {artist}\nThe track is: {track}")
        return ""
    else:
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            lyrics = str(soup.find(id="songLyricsDiv").text)
            lyrics = lyrics.replace("(instrumental)", "").replace("[instrumental]", "").replace("[Instrumental]", "").replace("(Instrumental)", "")
            if "do not have the lyrics for" in lyrics:
                logger.critical(f"Songlyrics doesn't have the lyrics for {track} by {artist}!")
                return ""
            else:
                logger.info(f"Successfully returning lyrics from songLyricsDiv div for {track} by {artist}")
                return str(soup.find(id="songLyricsDiv").text)
        except AttributeError:
            logger.critical(f"Failed finding the songLyricsDiv div for {track} by {artist}!")
            return ""

def songlyricsdotcom_format_strings(artist, track):
    regex_spec_characters = r"[ ,.!@#$%^&*()_+=/\\'\":;?\[\]]"

    no_space_artist = re.sub(regex_spec_characters, "", artist.replace(" ", "-").lower())
    no_space_track = re.sub(regex_spec_characters, "", track.replace(" ", "-").lower())

    if artist[0:2].lower() == "a ":
        no_space_artist = re.sub(regex_spec_characters, "", artist[2:].replace(" ", "-").lower())
    elif artist[0:4].lower() == "the ":
        no_space_artist = re.sub(regex_spec_characters, "", artist[3:].replace(" ", "-").lower())

    # special case handling
    featuring_filter = no_space_track.find("feat")
    if featuring_filter != -1:
        no_space_track = no_space_track[0:featuring_filter]

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

    return no_space_artist, no_space_track

def second_pass_lyrics():
    """
    Attempts to get a tracks lyrics, from the specified artist and album, via either the parse_azlyrics() or parse_songlyricsdotcom() function, selected by commenting, then attempting to add those lyrics to the database.
    This function is meant for 'stubborn' tracks that may have been missed by one parser or the other, or to which needed additional scraper refinement before being properly picked up..

    This function takes no parameters and returns no information.
    """

    for artist_name, album_title, track_title in dbcur.second_pass_empty_tracks():
        
        """
        Parser control mechanism is on the lines below

        AZLyrics provides better quality data
        Songlyrics.com features no bot protection
        """
        parsed_tracks = parse_azlyrics(artist_name, track_title)
        # parsed_tracks = parse_songlyricsdotcom(artist_name, track_title)
        resp = dbcur.add_track_lyrics(artist_name, album_title, track_title, parsed_tracks)
        if resp == NOT_FOUND:
            logger.critical(f"Either the track {track_title} or the album {album_title} from artist {artist_name} was not found!")
        elif resp == NO_ITEM_TO_ADD:
            logger.error(f"The track {track_title} on album {album_title} from artist {artist_name} has an empty string for its lyrics!  Check nulled 'lyrics' items in the database")
        else:
            logger.info(f"Successfully added {track_title}'s lyrics to the db.")
        time.sleep(10)


"""
Since this entire file is simply for database information population, these functions below are controlled based on commenting them in or out or by calling them from another file

At the current stage of dataset refinement (April 13, 2022): 

I'm currently focusing on manipulating the current dataset.
"""

logger = logging.getLogger('scraper_logger')
logger.setLevel(level=logging.WARNING)
dbcur = DbFunctions()

if __name__ == "__main__":
    logger.setLevel(level=logging.DEBUG)    # Allow manual runs to get more verbose information
    # add_artists()
    # get_albums()
    # get_tracks()
    # get_lyrics()
    # second_pass_lyrics()
    pass
