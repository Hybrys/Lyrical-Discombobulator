from bs4 import BeautifulSoup
import json
import requests

"""
Subscraper of Acclaimed Music's top 1000 artists
Splitting from each uri, which contains 200 artists, for easy debugging, and then concatenating with my own list for a 'master list'.
"""


def parse_table(uri):
    """
    Parse the table on Acclaimed Music websites with Beautiful Soup 4

    :param uri: The uri to parse
    :return result: A list of artists that were parsed from their table, and does not contain "/"
    """
    result = []

    response = requests.get(uri)
    soup = BeautifulSoup(response.text, 'html.parser')
    finder = soup.find("table")

    for element in finder.find_all("tr"):
        nexter = element.td.find_next_sibling("td")

        # Forward slashes were giving issues for obvious uri interference reasons, so I've decided to eliminate them as possible options for now
        # Second odd case - the band '!!!' was also giving major issues, so we're going to dismiss them for now.
        if nexter != None and nexter.a != None and nexter.a.text != "Albums" and "/" not in nexter.a.text and nexter.a.text != "!!!":
            result.append(nexter.a.text)
    return result


def join_jsons(number_of_results):
    """
    Concatenate the created jsons into one master list in json format

    :param number_of_results: The number of lists being joined together
    :output master_artist_list.json: A complete list of all parsed artists and a comment field with some notes
    """
    masterlist = []

    for i in range(number_of_results):
        artistjson = open(f"artist_list{i+1}.json")
        artistdata = json.load(artistjson)
        masterlist += artistdata["artists"]
    masterlist_for_json = {
        "__comment__": "List of around 1000 artists parsed from Acclaimed Music, plus 113 artists from my personal collection", "artists": masterlist}

    with open(f'master_artist_list.json', 'w') as output:
        json.dump(masterlist_for_json, output, indent=4)


result1 = parse_table("http://www.acclaimedmusic.net/061024/1948-09art.htm")
result2 = parse_table("http://www.acclaimedmusic.net/061024/1948-09art2.htm")
result3 = parse_table("http://www.acclaimedmusic.net/061024/1948-09art3.htm")
result4 = parse_table("http://www.acclaimedmusic.net/061024/1948-09art4.htm")
result5 = parse_table("http://www.acclaimedmusic.net/061024/1948-09art5.htm")

results = [result1, result2, result3, result4, result5]
for i, result in enumerate(results):
    result_for_json = {"artists": result}

    with open(f'artist_list{i+1}.json', 'w') as output:
        json.dump(result_for_json, output, indent=4)

join_jsons(6)
