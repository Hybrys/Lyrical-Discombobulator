from cmath import e
from logging import raiseExceptions
from bs4 import BeautifulSoup
import requests
import db
import json


def parse_album(artist):
    albums = []
    artist.replace(" ", "_")

    response = requests.get(
        f"https://en.wikipedia.org/wiki/{artist}_discography")
    soup = BeautifulSoup(response.text, 'html.parser')
    finder = find_album_list(soup)

    if finder == None:
        # print(f"Discog checked, trying {artist}_(band)")
        response = requests.get(
            f"https://en.wikipedia.org/wiki/{artist}_(band)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_album_list(soup)

    if finder == None:
        # print(f"Track listing wasn't found!  Trying just {artist}")
        response = requests.get(
            f"https://en.wikipedia.org/wiki/{artist}")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_album_list(soup)

    if response.status_code != 200:
        print(f"I'm {response.status_code}ing please send help")
        print(f"The artist is: {artist}")

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

            print(f"Successfully returning {artist} albums from tables")
            return albums

        except AttributeError:
            # print(f"I didn't find a Studio Album table for {artist}, trying Discography")
            pass

        try:
            lister = finder.parent.find_next_sibling("ul")
            for element in lister:
                if element.name != None:
                    albums.append(element.i.text)
            print(f"Successfully returning {artist} albums from discog")
            return albums
        except AttributeError:
            print(f"I failed parsing any albums for {artist}")


def parse_tracks(artist, album):
    """
    Parses a list of tracks from an album by a particular artist

    :param album: Title of the album as a string
    :param artist: Name of the artist that the album belongs to as a string
    """

    tracks = []
    artist.replace(" ", "_")
    album.replace(" ", "_")

    response = requests.get(
        f"https://en.wikipedia.org/wiki/{album}")
    soup = BeautifulSoup(response.text, 'html.parser')
    finder = find_track_list(soup)

    if finder == None:
        # print(f"Track listing wasn't found!  Trying (album) for {album}")
        response = requests.get(
            f"https://en.wikipedia.org/wiki/{album}_(album)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_track_list(soup)

    if finder == None:
        # print(f"Track listing wasn't found!  Trying ({artist}_album) for {album}")
        response = requests.get(
            f"https://en.wikipedia.org/wiki/{album}_({artist}_album)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_track_list(soup)

    if finder == None:
        # print(f"I still can't find anything for {artist}'s album {album}")
        return tracks

    if response.status_code != 200:
        print(f"I'm {response.status_code}ing please send help")
        print(f"The artist is: {artist}\nThe album is: {album}")

    else:
        tabler = finder.parent.find_next_sibling("table")
        lister = finder.parent.find_next_sibling("ol")
        if tabler:
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
            return tracks

        elif lister:
            print(
                f"I didn't find a table for {album}, but I found an ordered list!")
            for element in lister("li"):
                hyphen = element.text.find("–")
                tracks.append((element.text[:hyphen-1].replace('"', '')))
            return tracks
        else:
            print("Whelp, I broke")


def find_album_list(soup):
    finder = soup.find(id="Studio_albums")
    # print("1", finder)
    if finder != None:
        return finder
    finder = soup.find(id="Studio_album")
    # print("2", finder)
    if finder != None:
        return finder
    finder = soup.find(id="Discography")
    # print("3", finder)
    if finder != None:
        return finder
    finder = soup.find(id="Albums")
    # print("4", finder)
    if finder != None:
        return finder
    # print("helper failed out")
    return None


def find_track_list(soup):
    finder = soup.find(id="Track_listing")
    # print("1", finder)
    if finder != None:
        return finder
    finder = soup.find(id="tracklist")
    # print("2", finder)
    if finder != None:
        return finder
    finder = soup.find(class_="tracklist")
    # print("3", finder)
    if finder != None:
        return finder
    return None


dbcur = db.DbFunctions()
artistjson = open("artistlist.json")
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
    if parsed_artists[artist] != None:
        resp = dbcur.add_artist(artist, parsed_artists[artist])
        if resp == db.NAME_COLLIDED:
            print("I collided with a name in the db!")
        for album in parsed_artists[artist]:
            parsed_albums[album] = parse_tracks(artist, album)
            # print(parsed_albums[album])

# for artist in parsed_artists:
            # print(artist, " ", album)
            # print(f"\t{parsed_albums[album]}")
