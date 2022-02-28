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


dbcur = db.DbFunctions()

artists = ["Death Cab for Cutie", "Spitalfield", "Interpol", "Metric",
           "Crash Test Dummies", "The Juliana Theory", "Amber Pacific"]
parsed_artists = {}

for artist in artists:
    parsed_artists[artist] = parse_album(artist)

for artist in parsed_artists:
    resp = dbcur.add_artist(artist, parsed_artists[artist])
    if resp == db.NAME_COLLIDED:
        print("I collided with a name in the db!")

    for album in parsed_artists[artist]:
        # album parsing songs goes here
        pass
