"""TODO
    INPROGRESS
    1. Parse lyrics very slowly.
    2. 'Front' 'end'

    WOULD BE NICE
    1. Oh my god unittesting
    2. Better non-unicode handling (oomlots and accents)
    3. Handle typeerroring cases
    4. Create handler for cases that are not properly parsing for later analysis
    5. Backtracking refactor (parse whole pages)
    6. Add timecodes to tracks
    7. Swap the parser from html.parser to lxml for ~25% speedup on wiki parses
"""

from unittest import result
from itty3 import HTML, App, HttpResponse
from urllib.parse import unquote, quote

from jmespath import search
import db

app = App()
database = db.DbFunctions()


@app.get("/")
def index(request):
    with open("index.html") as index_file:
        result = index_file.read()
    return app.render(request, result)


@app.get("/artist/<str:artist>")
def view_artist(request, artist):
    response = ["<table><tr><th>Artist</th><th>Album</th></tr>"]
    artist = unquote(artist)
    check = database.view_artist_albums(artist)
    if check != db.NOT_FOUND:
        for artist_name, album_name in check:
            album_uri = quote(album_name)
            response.append(f"<tr><td>{artist_name}</td><td><a href=# onclick='$(\"#div1\").load(\"album/{album_uri}\")'>{album_name}</a></td></tr>")
        response = "".join(response) + "</table>"
        return HttpResponse(body=response, content_type=HTML)

    else:
        response = ["Did you mean one of the following artists?<br/>"]
        searchlen = len(artist)
        if searchlen <= 5:
            artist = artist[int(searchlen/2)::]
        check = database.view_artist_albums_fuzzy(artist)
        if check == db.NOT_FOUND:
            return HttpResponse(body="This artist isn't in the database yet!", content_type=HTML)
        for fetched_item in check:
            print(fetched_item)
            artist = quote(fetched_item[0])
            response.append(f"<br/><a href=# onclick='$(\"#div1\").load(\"artist/{artist}\")'>{fetched_item[0]}</a>")
            response = "".join(response)
            return HttpResponse(body=response, content_type=HTML)


@app.get("/album/<str:album>")
def view_album(request, album):
    response = ["<table><tr><th>Artist</th><th>Album</th><th>Track</th></tr>"]
    album = unquote(album)
    check = database.view_album_tracks(album)
    if check != db.NOT_FOUND:
        for artist_name, album_title, track in check:
            track_uri = quote(track[0])
            artist_uri = quote(artist_name)
            album_uri = quote(album_title)
            response.append(f"<tr><td>{artist_name}</td><td>{album_title}</td><td><a href=# onclick='$(\"#div1\").load(\"track/{track_uri}/{artist_uri}/{album_uri}\")'>{track[0]}</a></td></tr>")
        response = "".join(response) + "</table>"
        return HttpResponse(body=response, content_type=HTML)

    else:
        response = ("Did you mean one of the following albums?\n")
        searchlen = len(album)
        if searchlen <= 5:
            album_query = album[int(searchlen/2)::]
        check = database.view_album_tracks_fuzzy(album_query)
        print(check)
        if check == db.NOT_FOUND:
            return HttpResponse(body="This album isn't in the database yet!", content_type=HTML)
        for album in check:
            album_uri = quote(album)
            response.append(f"\n<a href=# onclick='$(\"#div1\").load(\"album/{album_uri}\")'>{album}</a>")
        response = "".join(response)
        return HttpResponse(body=response, content_type=HTML)


@app.get("/track/<str:track>/<str:artist>/<str:album>")
def view_track(request, track, artist, album):
    track = unquote(track)
    artist = unquote(artist)
    album = unquote(album)

    check, result = database.view_track_lyrics(track, artist, album)

    if check == db.SUCCESS_NO_RESPONSE:
        print(result)
        for track, lyrics, artist_name, album_title in result:
            lyrics = lyrics.replace("\n", "<br/>")
            response = f"<table><tr><th>Artist</th><th>Album</th><th>Track</th></tr><tr><td>{artist_name}</td><td>{album_title}</td><td>{track}</td></tr></table><br/><br/>{lyrics}"
        response = "".join(response)
        return HttpResponse(body=response, content_type=HTML)

    if check == db.MANY_FOUND:
        response = ["I found a couple of songs with the same name.  Please select the correct one below:", "<table><tr><th>Artist</th><th>Album</th><th>Track</th></tr>"]
        for track, artist_name, album_title in result:
            track_uri = quote(track)
            artist_uri = quote(artist_name)
            album_uri = quote(album_title)
            response.append(f"<tr><td>{artist_name}</td><td>{album_title}</td><td><a href=# onclick='$(\"#div1\").load(\"track/{track_uri}/{artist_uri}/{album_uri}\")'>{track}</a></td></tr>")
        response = "".join(response) + "</table>"
        return HttpResponse(body=response, content_type=HTML)

    else:
        return HttpResponse(body="How did I even get here?!", content_type=HTML)

    # else:
    #     response = ("Did you mean one of the following albums?\n")
    #     searchlen = len(album)
    #     if searchlen <= 5:
    #         album_query = album[int(searchlen/2)::]
    #     check = database.view_album_tracks_fuzzy(album_query)
    #     print(check)
    #     if check == db.NOT_FOUND:
    #         return HttpResponse(body="This album isn't in the database yet!", content_type=HTML)
    #     for album in check:
    #         album_uri = quote(album)
    #         response.append(f"\n<a href=# onclick='$(\"#div1\").load(\"album/{album_uri}\")'>{album}</a>")
    #     response = "".join(response)
    #     return HttpResponse(body=response, content_type=HTML)


if __name__ == "__main__":
    app.run(port=4000, debug=True)
