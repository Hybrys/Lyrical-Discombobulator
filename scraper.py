from cmath import e
from logging import raiseExceptions
from bs4 import BeautifulSoup
import requests
import db


def parse_album(artist):
    albums = []
    artist.replace(" ", "_")

    response = requests.get(
        f"https://en.wikipedia.org/wiki/{artist}_discography")

    if response.status_code == 404:
        response = requests.get(f"https://en.wikipedia.org/wiki/{artist}")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            finder = soup.find(
                id="Studio_albums").parent.find_next_sibling("table")
            first_col = finder.tbody.tr.th.text.rstrip().lower()

            if first_col == "year":
                for element in finder.tbody("tr"):
                    if element.td != None and element.td.next_sibling != None:
                        albums.append(
                            element.td.next_sibling.next_sibling.i.text)

            elif first_col == "title":
                for element in finder.tbody("tr"):
                    if element.td != None and element.td.find_previous_sibling("th") != None:
                        albums.append(
                            element.td.find_previous_sibling("th").i.text)
            return albums
        except:
            print(
                f"I didn't find a Studio Album table for {artist}, trying Discography")

        try:
            finder = soup.find(
                id="Discography").parent.next_sibling.next_sibling.next_sibling.next_sibling
            for element in finder:
                if element.name != None:
                    albums.append(element.i.text)
            return albums
        except:
            print(f"I didn't find a Discography table for {artist} either!")


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
        print("Track listing wasn't found!  Trying (album)")
        response = requests.get(
            f"https://en.wikipedia.org/wiki/{album}_(album)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_track_list(soup)

    if finder == None:
        print(f"Track listing wasn't found!  Trying ({artist}_album)")
        response = requests.get(
            f"https://en.wikipedia.org/wiki/{album}_({artist}_album)")
        soup = BeautifulSoup(response.text, 'html.parser')
        finder = find_track_list(soup)

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
                f"I didn't find a table for {artist}, but I found an ordered list!")
            for element in lister("li"):
                hyphen = element.text.find("–")
                tracks.append((element.text[:hyphen-1].replace('"', '')))
            return tracks
        else:
            print("Whelp, I broke")


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

artists = ["Death Cab for Cutie", "Spitalfield", "Interpol", "Metric",
           "Crash Test Dummies", "The Juliana Theory", "Amber Pacific"]
parsed_artists = {}
parsed_albums = {}

for artist in artists:
    parsed_artists[artist] = parse_album(artist)

for artist in parsed_artists:
    resp = dbcur.add_artist(artist, parsed_artists[artist])
    if resp == db.NAME_COLLIDED:
        print("I collided with a name in the db!")

for artist in parsed_artists:
    for album in parsed_artists[artist]:
        parsed_albums[album] = parse_tracks(artist, album)
        # print(artist, " ", album)
        # print(f"\t{parsed_albums[album]}")
