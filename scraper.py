from bs4 import BeautifulSoup
import requests
import db
import json
import logging

"""TODO
    MUSTS
    1. Tracks into the DB!
    2. Parse lyrics!
    3. Lyrics into the DB!
    4. 'Front' 'end'
    
    WOULD BE NICE
    1. Handle typeerroring cases
    2. Create handler for cases that are not properly parsing for later analysis (DB?)
    3. Backtracking refactor (parse whole pages)
    4. Add timecodes to tracks
"""


def parse_album(artist):
    albums = []
    artist = artist.replace(" ", "_")

    response = requests.get(
        f"https://en.wikipedia.org/wiki/{artist}_discography")
    soup = BeautifulSoup(response.text, 'html.parser')
    finder = find_album_list(soup)

    if finder == None:
        logging.debug(f"Discog checked, trying {artist}_(band)")
        response = requests.get(
            f"https://en.wikipedia.org/wiki/{artist}_(band)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_album_list(soup)

    if finder == None:
        logging.debug(f"Track listing wasn't found!  Trying just {artist}")
        response = requests.get(
            f"https://en.wikipedia.org/wiki/{artist}")
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
            logging.debug(
                f"Failed to retrieve {artist}s albums from a table, trying a list")
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

    response = requests.get(
        f"https://en.wikipedia.org/wiki/{album}")
    soup = BeautifulSoup(response.text, 'html.parser')
    finder = find_track_list(soup)

    if finder == None:
        logging.debug(
            f"Track listing wasn't found!  Trying (album) for {album}")
        response = requests.get(
            f"https://en.wikipedia.org/wiki/{album}_(album)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_track_list(soup)

    if finder == None:
        logging.debug(
            f"Track listing wasn't found!  Trying ({artist}_album) for {album}")
        response = requests.get(
            f"https://en.wikipedia.org/wiki/{album}_({artist}_album)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_track_list(soup)

    if finder == None:
        logging.error(
            f"I still can't find a wiki page for {artist}'s album {album}")
        return tracks

    if response.status_code != 200:
        logging.critical(f"I'm {response.status_code}ing please send help")
        logging.critical(f"The artist is: {artist}\nThe album is: {album}")

    else:
        try:
            tabler = finder.parent.find_next_sibling("table")
            if tabler.tbody.tr.th != None:
                first_col = tabler.tbody.tr.th.text.rstrip().lower()
                if first_col == "no.":
                    for element in tabler.tbody("tr"):
                        if element.td != None and element.td.find_next_sibling("td") != None:
                            tracks.append(
                                element.td.text.replace('"', ''))

                elif first_col == "title":
                    for element in tabler.tbody("tr"):
                        if element.td != None and element.td.find_previous_sibling("th") != None:
                            tracks.append(
                                element.td.find_previous_sibling("th").i.text)
            logging.info(
                f"Successfully returning tracks for {album} from a table!")
            return tracks
        except AttributeError:
            pass

        try:
            lister = finder.parent.find_next_sibling("ol")
            logging.info(
                f"I didn't find a table for {album}, but I found an ordered list!")
            for element in lister("li"):
                hyphen = element.text.find("–")
                tracks.append((element.text[:hyphen-1].replace('"', '')))
            logging.info(
                f"Successfully returning tracks for {album} from a list!")
            return tracks
        except AttributeError:
            logging.error(
                f"Whelp, I broke trying to parse {artist}'s album titled {album}")
        except TypeError:
            logging.error(
                f"I typeerrored out trying to parse the album {album} from {artist}")


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


logging.basicConfig(level=logging.CRITICAL)

dbcur = db.DbFunctions()
artistjson = open("artist_list1.json")
artistdata = json.load(artistjson)
artists = artistdata["artists"]

# Manual override for focused testing
# artists = ["Bright Eyes", "Lotus Child",
#    "Thursday"]
# artists = ["Bright Eyes"]

parsed_artists = {}
parsed_albums = {}

for artist in artists:
    parsed_artists[artist] = parse_album(artist)

for artist in parsed_artists:
    resp = dbcur.add_artist_albums(artist, parsed_artists[artist])
    if resp == db.NAME_COLLIDED:
        logging.debug(f"I collided with a name in the db for {artist}")
    elif resp == db.NO_ITEM_IN_LIST:
        logging.error(f"There were no albums in the list for artist {artist}")
    else:
        logging.info(f"Successfully added {artist} albums to the db.")

    if parsed_artists[artist] != None:
        for album in parsed_artists[artist]:
            parsed_albums[album] = parse_tracks(artist, album)
            resp = dbcur.add_album_tracks(artist, album, parsed_albums[album])
            if resp == db.NOT_FOUND:
                logging.critical(f"The artist {artist} and album {album} were not found while trying to add tracks to the database!")
            elif resp == db.NO_ITEM_IN_LIST:
                logging.error(f"The album {album} from artist {artist} has an empty list for its tracks.  Check nulled 'isparsed' items later!")
            else:
                logging.info(f"Successfully added {album} had its tracks added to the db.")
    else:
        logging.error(f"This artist {artist} has 'Nonetype' albums!")
