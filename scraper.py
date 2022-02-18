from bs4 import BeautifulSoup
import requests


def parse_album(artist):
    albooms = []
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
                        albooms.append(
                            element.td.next_sibling.next_sibling.i.text)

            elif first_col == "title":
                for element in finder.tbody("tr"):
                    if element.td != None and element.td.find_previous_sibling("th") != None:
                        albooms.append(
                            element.td.find_previous_sibling("th").i.text)
            return albooms
        except:
            print(
                f"I didn't find a Studio Album table for {artist}, trying Discography")

        try:
            finder = soup.find(
                id="Discography").parent.next_sibling.next_sibling.next_sibling.next_sibling
            for element in finder:
                if element.name != None:
                    albooms.append(element.i.text)
            return albooms
        except:
            print(f"I didn't find a Discography table for {artist} either!")


artists = ["Death Cab for Cutie", "Spitalfield", "Interpol", "Metric",
           "Crash Test Dummies", "The Juliana Theory", "Amber Pacific"]
letsparse = {}

for artist in artists:

    letsparse[artist] = parse_album(artist)

# print(parse_album("The Juliana Theory"))
for artist in letsparse:
    print(artist)
    print("\t", letsparse[artist])
