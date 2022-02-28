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

    if soup.find(id="Track_listing") == None:
        print("Track listing wasn't found!  Is this even an album page?!")
        response = requests.get(
            f"https://en.wikipedia.org/wiki/{album}_({artist}_album)")

    if response.status_code == 200:
        try:
            try:
                finder = soup.find(
                    id="Track_listing").parent.find_next_sibling("table")
            except AttributeError:
                print(
                    "I couldn't find a track_listing, these assholes did something else!")
                finder = soup.find("table", class_="tracklist")
                print(finder, "this is the tracklist finder")

            first_col = finder.tbody.tr.th.text.rstrip().lower()

            if first_col == "no.":
                for element in finder.tbody("tr"):
                    if element.td != None and element.td.find_next_sibling("td") != None:
                        print(element.td.text.replace('"', ''))
                        print(element.td.find_next_sibling("td").text)
                        tracks.append(
                            element.td.text.replace('"', ''))

            elif first_col == "title":
                for element in finder.tbody("tr"):
                    if element.td != None and element.td.find_previous_sibling("th") != None:
                        tracks.append(
                            element.td.find_previous_sibling("th").i.text)
            return tracks

        except AttributeError:
            print(
                f"I didn't find a table for {artist}, trying without tables!")
            try:
                finder = soup.find(
                    id="Track_listing").parent.find_next_sibling("ol")
            except AttributeError:
                finder = soup.find(
                    id="tracklist").parent.find_next_sibling("ol")
            for element in finder("li"):
                hyphen = element.text.find("–")
                tracks.append((element.text[:hyphen-1].replace('"', '')))
            return tracks

        except Exception as e:
            raise e

    else:
        print(f"I'm {response.status_code}ing please send help")


# dbcur = db.DbFunctions()

# artists = ["Death Cab for Cutie", "Spitalfield", "Interpol", "Metric",
#            "Crash Test Dummies", "The Juliana Theory", "Amber Pacific"]
# parsed_artists = {}

# for artist in artists:
#     parsed_artists[artist] = parse_album(artist)

# for artist in parsed_artists:
#     resp = dbcur.add_artist(artist, parsed_artists[artist])
#     if resp == db.NAME_COLLIDED:
#         print("I collided with a name in the db!")

#     for album in parsed_artists[artist]:
#         # album parsing songs goes here
#         pass

parsed_artists = {"Death Cab for Cutie": [
    "Codes and Keys"], "Spitalfield": ["Stop Doing Bad Things"], "The Juliana Theory": ["Love"]}
parsed_albums = {}

for artist in parsed_artists:
    for album in parsed_artists[artist]:
        parsed_albums[album] = parse_tracks(artist, album)
        print(artist, " ", album)
        print(f"\t{parsed_albums[album]}")
