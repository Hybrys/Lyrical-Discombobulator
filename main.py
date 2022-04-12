"""
Simple frontend for the data gathered by scraper.py utilizing Flask for web functionality

Port 4000
Debug currently True
"""

# Resolve modules not loading
import os
import sys
sys.path.append(os.getcwd())

from flask import Flask, Response
from urllib.parse import unquote, quote
from db.db_postgres import DbFunctions, NOT_FOUND, NAME_COLLIDED, NO_ITEM_TO_ADD, SUCCESS_NO_RESPONSE, MANY_FOUND, NO_CONTENT

app = Flask(__name__)
database = DbFunctions()

@app.get("/")
def index():
    """
    Serves the / route with the index.html file included in the project

    This file is a simple HTML / JQuery build, allowing for a psuedo-responsive page that's as lightweight as possible.
    The index should allow for any cross navigation without needing to leave the single page, and loads any information into a seperate div.

    :return: Returns the webpage using the Response() class from Flask
    """
    with open("./index.html") as index_file:
        result = index_file.read()
    return Response(result)


@app.get("/artist/<string:artist>")
def view_artist(artist):
    """
    Serves the /artist/ route, accepting the next part of the URI as an argument

    The function uses the <string:artist> part of the URI for looking up an artist.  If an exact match is not found, it tries a pseudo-fuzzy search to find relevant partial matches to respond with.  If no matches are found again, it returns a statement to that effect.

    :param artist: Accepts the information in the <string:artist> area of the URI, in order to perform the lookup function
    :return: Returns the response webpage using the Response() class from Flask
    """
    response = ["<table><tr><th>Artist</th><th>Album</th></tr>"]
    artist = unquote(artist)
    check = database.view_artist_albums(artist)
    if check != NOT_FOUND:
        for artist_name, album_title in check:
            artist_link, album_link, track_link = convert_link_strings(artist_name, album_title, "!")
            response.append(f"<tr><td>{artist_name}</td>")
            response.append(album_link + "</tr>")
        response = "".join(response) + "</table>"
        return Response(response)

    else:
        response = ["Did you mean one of the following artists?<br/>"]
        searchlen = len(artist)
        if searchlen >= 5:
            artist = artist[int(searchlen/2)::]
        check = database.view_artist_albums_fuzzy(artist)
        if check == NOT_FOUND:
            return Response("This artist isn't in the database yet!  Maybe we'll add it soon?", status=400)
        for fetched_item in check:
            artist = quote(fetched_item[0])
            response.append(f"<br/><a href=# onclick='$(\"#div1\").load(\"artist/{artist}\")'>{fetched_item[0]}</a>")
        response = "".join(response)
        return Response(response)


@app.get("/album/<string:album>")
def view_album(album):
    """
    Serves the /album/ route, accepting the next part of the URI as an argument

    The function uses the <string:album> part of the URI for looking up an album title.  If an exact match is not found, it tries a pseudo-fuzzy search to find relevant partial matches to respond with.  If no matches are found again, it returns a statement to that effect.

    :param album: Accepts the information in the <string:album> area of the URI, in order to perform the lookup function
    :return: Returns the response webpage using the Response() class from Flask
    """
    response = ["<table><tr><th>Artist</th><th>Album</th><th>Track</th></tr>"]
    album = unquote(album)
    check = database.view_album_tracks(album)
    if check != NOT_FOUND and check != NO_CONTENT:
        for artist_name, album_title, track_title in check:
            artist_link, album_link, track_link = convert_link_strings(artist_name, album_title, track_title)
            response.append(artist_link)
            response.append(f"<td>{album_title}</td>")
            response.append(track_link)
        response = "".join(response) + "</table>"
        return Response(response)

    elif check == NOT_FOUND:
        response = ["Did you mean one of the following albums?<br />"]
        searchlen = len(album)
        if searchlen >= 5:
            album = album[int(searchlen/2)::]
        check = database.view_album_tracks_fuzzy(album)
        if check == NOT_FOUND:
            return Response("This album isn't in the database yet!", status=400)
        for res_album in check:
            album_uri = quote(res_album[2])
            response.append(f"<br /><a href=# onclick='$(\"#div1\").load(\"album/{album_uri}\")'>{res_album[2]}</a>")
        response = "".join(response)
        return Response(response)

    else:
        return Response(f"The album {album} has no tracks in it yet!  Sorry!", status=400)


@app.get("/track/<string:track>/<string:artist>/<string:album>")
def view_track(track, artist, album):
    """
    Serves the /track/ route, accepting the next parts of the URI as an argument, each between a set of /
    By default, index.html will only search for the track with the first argument, using '!' to denote "novalue" for the second and third arguments.
    These arguments are kept for direct linking in the case of name collision of a track title

    The function uses the <string:track> part of the URI for looking up a tracks title.  If more than one match is found, it will return a table of the tracks with their artists and albums, with clickable links to each element.
    If no matches are found, it then returns a statement to that affect.  If the track has no data in the Lyrics field, it then returns a statement to that affect.

    :param album: Accepts the information in the <string:track> area of the URI, in order to perform the lookup function
    :param artist: Accepts the information in the <string:artist> area of the URI, in order to perform the lookup function
    :param album: Accepts the information in the <string:album> area of the URI, in order to perform the lookup function
    :return: Returns the response webpage using the Response() class from Flask
    """
    response = ["<table><tr><th>Artist</th><th>Album</th><th>Track</th></tr>"]
    track = unquote(track)
    artist = unquote(artist)
    album = unquote(album)
    empty_track = False

    check, result = database.view_track_lyrics(track, artist, album)

    if check == SUCCESS_NO_RESPONSE:
        for track_title, lyrics, artist_name, album_title in result:
            if lyrics == None:
                lyrics = f"We don't have lyrics for {track_title} yet!  Sorry!"
                empty_track = True
            response.extend(convert_link_strings(artist_name, album_title, track_title)[0:2])
            lyrics = lyrics.replace("\n", "<br/>")
            response.append(f"<td>{track_title}</td></tr></table><br/><br/>{lyrics}")
        response = "".join(response)
        if empty_track == True:
            return Response(response, status=400)
        return Response(response)

    elif check == MANY_FOUND:
        response = ["I found a couple of songs with the same name.  Please select the correct one below:", "<table><tr><th>Artist</th><th>Album</th><th>Track</th></tr>"]
        for track_title, artist_name, album_title in result:
            response.extend(convert_link_strings(artist_name, album_title, track_title))
        response = "".join(response) + "</table>"
        return Response(response)

    else:
        return Response("This track isn't in the database yet!  Sorry!", status=400)


@app.get("/lyrics/<string:searchparam>")
def lyric_lookup(searchparam):
    """
    Serves the /lyrcs/ route, accepting the next part of the URI as an argument

    The function uses the <string:searchparam> part of the URI for looking up a tracks that have lyrics matching the word or phrase.  If it finds any tracks whos lyrics contain searchparam, it will return a table of the tracks with their artists and albums, with clickable links to each element.
    If no matches are found, it then returns a statement to that affect.

    :param searchparam: Accepts the information in the <string:searchparam> area of the URI, in order to perform the lookup function
    :return: Returns the response webpage using the Response() class from Flask
    """
    searchparam = unquote(searchparam)
    response = [f"These are the tracks that have the word or phrase '{searchparam}' in its lyrics:<br />", "<table><tr><th>Artist</th><th>Album</th><th>Track</th></tr>"]

    check = database.lyric_lookup(searchparam)
    if check == NOT_FOUND:
        return Response("I couldn't find any tracks with that word/phrase in it.  Sorry!", status=400)
    for artist_name, album_title, track_title in check:
        response.extend(convert_link_strings(artist_name, album_title, track_title))
    response = "".join(response) + "</table>"
    return Response(response)


def convert_link_strings(artist_name, album_title, track_title):
    """
    Helper function for creating the table elements with clickable links

    :param artist_name: The artist name item from the DB response as a string
    :param album_title: The album title item from the DB response as a string
    :param track_title: The track_title item from the DB response as a string, or a "!" in cases that the track is irrelevant
    :return: A list of strings for the artist, album, and track links, built into a single table row
    """
    result = []
    track_uri = quote(track_title)
    artist_uri = quote(artist_name)
    album_uri = quote(album_title)
    result.append(f"<tr><td><a href=# onclick='$(\"#div1\").load(\"artist/{artist_uri}\")'>{artist_name}</a></td>")
    result.append(f"<td><a href=# onclick='$(\"#div1\").load(\"album/{album_uri}\")'>{album_title}</a></td>")
    result.append(f"<td><a href=# onclick='$(\"#div1\").load(\"track/{track_uri}/{artist_uri}/{album_uri}\")'>{track_title}</a></td></tr>")
    return result

def db_closer():
    database.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)