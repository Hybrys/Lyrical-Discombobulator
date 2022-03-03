from bs4 import BeautifulSoup
from requests_ip_rotator import ApiGateway, ALL_REGIONS
import re
import requests
import db
import json
import logging


"""TODO
    MUSTS
    1. Parse lyrics with a new website!
    2. 'Front' 'end'

    WOULD BE NICE
    1. Handle typeerroring cases
    2. Create handler for cases that are not properly parsing for later analysis (DB?)
    3. Backtracking refactor (parse whole pages)
    4. Add timecodes to tracks
    5. Swap the parser from html.parser to lxml
"""


def parse_album(artist):
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
    Parses a list of tracks from an album by a particular artist

    :param album: Title of the album as a string
    :param artist: Name of the artist that the album belongs to as a string
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


def parse_lyrics(artist, track, session):
    no_space_artist = artist.replace(" ", "").lower()
    no_space_track = track.lower()
    no_space_track = re.sub(r"[ ,.!@#$%^&*()_+=\-/\\'\":;]", "", no_space_track)

    if artist[0:2].lower() == "a ":
        no_space_artist = re.sub(r"[ ,.!@#$%^&*()_+=\-/\\'\":;]", "", artist[2:].lower())

    featuring_filter = no_space_track.find("feat")
    if featuring_filter != -1:
        no_space_track = no_space_track[0:featuring_filter]

    while True:
        try:
            response = session.get(f"https://www.azlyrics.com/lyrics/{no_space_artist}/{no_space_track}.html")
            break
        except requests.RequestException:
            continue

    if response.status_code != 200:
        logging.critical(f"I'm {response.status_code}ing please send help")
        logging.critical(f"The artist is: {artist}\nThe track is: {track}")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            soup = soup.find(class_="lyricsh").find_next_sibling("b")
            div_string = str(soup.find_next_sibling("div"))
            comment_tag = div_string.find("-->")
            lyrics = div_string[comment_tag+3:].replace("</div>", "").replace("<br/>", "").replace("\r", "")
            return lyrics[1:-2]
        except AttributeError:
            logging.critical(f"Failed finding the lyricsh div for {track} by {artist}!")
            return ""


def find_album_list(soup):
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


logging.basicConfig(level=logging.DEBUG)

dbcur = db.DbFunctions()
artistjson = open("artist_list6.json")
artistdata = json.load(artistjson)
artists = artistdata["artists"]

# Manual override for focused testing
# artists = ["Bright Eyes", "Lotus Child",
#    "Thursday"]
# artists = ["Bright Eyes"]

parsed_artists = {}
parsed_albums = {}
parsed_tracks = {}

for artist in artists:
    resp = dbcur.add_artist(artist)
    if resp == db.NAME_COLLIDED:
        logging.debug(f"I collided with a name in the db for {artist}")
    else:
        logging.info(f"Successfully added {artist} to the db.")

for artist in dbcur.view_unparsed_artists():
    parsed_artists[artist] = parse_album(artist[0])
    resp = dbcur.add_artist_albums(artist, parsed_artists[artist])

for album in dbcur.view_unparsed_albums():
    parsed_albums[album[0]] = parse_tracks(album[1], album[0])
    resp = dbcur.add_album_tracks(album[1], album[0], parsed_albums[album[0]])
    if resp == db.NOT_FOUND:
        logging.critical(f"The artist {album[1]} and album {album[0]} were not found while trying to add tracks to the database!")
    elif resp == db.NO_ITEM_TO_ADD:
        logging.error(f"The album {album[0]} from artist {album[1]} has an empty list for its tracks.  Check Falsed 'isparsed' items in the database")
    else:
        logging.info(f"Successfully added {album[0]} had its tracks added to the db.")


# AZLyrics didn't like me after about 25 requests
# Even slowing down to one per 5sec resulted in an IP ban in under 1min
# User_agent modding also had no effect

with ApiGateway("https://www.azlyrics.com", regions=ALL_REGIONS, access_key_id=, access_key_secret=) as gateway:
    session = requests.Session()
    session.mount("https://www.azlyrics.com", gateway)
    for i, track in enumerate(dbcur.view_unparsed_tracks()):
        parsed_tracks[track[2]] = parse_lyrics(track[0], track[2], session)

        resp = dbcur.add_track_lyrics(track[0], track[1], track[2], parsed_tracks[track[2]])
        if resp == db.NOT_FOUND:
            logging.critical(f"Either the track {track[2]} or the album {track[1]} from artist {track[0]} was not found!")
        elif resp == db.NO_ITEM_TO_ADD:
            logging.error(f"The track {track[2]} on album {track[1]} from artist {track[0]} has an empty string for its lyrics!  Check nulled 'lyrics' items in the database")
        else:
            logging.info(f"Successfully added {track[2]}'s lyrics added to the db.")
