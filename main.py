"""TODO
    INPROGRESS
    1. Parse lyrics very slowly.

    WOULD BE NICE
    1. Oh my god unittesting
    2. Better non-unicode handling (oomlots and accents)
    3. Handle typeerroring cases
    4. Create handler for cases that are not properly parsing for later analysis
    5. Backtracking refactor (parse whole pages)
    6. Add timecodes to tracks
    7. Swap the parser from html.parser to lxml for ~25% speedup on wiki parses
"""

from itty3 import HTML, App, HttpResponse
from urllib.parse import unquote, quote
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
        for artist_name, album_title in check:
            artist_link, album_link, track_link = convert_link_strings(artist_name, album_title, "!")
            response.append(f"<tr><td>{artist_name}</td>")
            response.append(album_link + "</tr>")
        response = "".join(response) + "</table>"
        return HttpResponse(body=response, content_type=HTML)

    else:
        response = ["Did you mean one of the following artists?<br/>"]
        searchlen = len(artist)
        if searchlen >= 5:
            artist = artist[int(searchlen/2)::]
        check = database.view_artist_albums_fuzzy(artist)
        if check == db.NOT_FOUND:
            return HttpResponse(body="This artist isn't in the database yet!  Maybe we'll add it soon?", content_type=HTML)
        for fetched_item in check:
            artist = quote(fetched_item[0])
            response.append(f"<br/><a href=# onclick='$(\"#div1\").load(\"artist/{artist}\")'>{fetched_item[0]}</a>")
        response = "".join(response)
        return HttpResponse(body=response, content_type=HTML)


@app.get("/album/<str:album>")
def view_album(request, album):
    response = ["<table><tr><th>Artist</th><th>Album</th><th>Track</th></tr>"]
    album = unquote(album)
    check = database.view_album_tracks(album)
    if check != db.NOT_FOUND and check != db.NO_CONTENT:
        for artist_name, album_title, track_title in check:
            artist_link, album_link, track_link = convert_link_strings(artist_name, album_title, track_title[0])
            response.append(artist_link)
            response.append(f"<td>{album_title}</td>")
            response.append(track_link)
        response = "".join(response) + "</table>"
        return HttpResponse(body=response, content_type=HTML)

    elif check == db.NOT_FOUND:
        response = ["Did you mean one of the following albums?<br />"]
        searchlen = len(album)
        if searchlen >= 5:
            album = album[int(searchlen/2)::]
        check = database.view_album_tracks_fuzzy(album)
        if check == db.NOT_FOUND:
            return HttpResponse(body="This album isn't in the database yet!", content_type=HTML)
        for res_album in check:
            album_uri = quote(res_album[2])
            response.append(f"<br /><a href=# onclick='$(\"#div1\").load(\"album/{album_uri}\")'>{res_album[2]}</a>")
        response = "".join(response)
        return HttpResponse(body=response, content_type=HTML)

    else:
        return HttpResponse(body=f"The album {album} has no tracks in it yet!  Sorry!", content_type=HTML)


@app.get("/track/<str:track>/<str:artist>/<str:album>")
def view_track(request, track, artist, album):
    response = ["<table><tr><th>Artist</th><th>Album</th><th>Track</th></tr>"]
    track = unquote(track)
    artist = unquote(artist)
    album = unquote(album)

    check, result = database.view_track_lyrics(track, artist, album)

    if check == db.SUCCESS_NO_RESPONSE:
        for track_title, lyrics, artist_name, album_title in result:
            if lyrics == None:
                lyrics = f"We don't have lyrics for {track_title} yet!  Sorry!"
            response.extend(convert_link_strings(artist_name, album_title, track_title)[0:2])
            lyrics = lyrics.replace("\n", "<br/>")
            response.append(f"<td>{track_title}</td></tr></table><br/><br/>{lyrics}")
        response = "".join(response)
        return HttpResponse(body=response, content_type=HTML)

    elif check == db.MANY_FOUND:
        response = ["I found a couple of songs with the same name.  Please select the correct one below:", "<table><tr><th>Artist</th><th>Album</th><th>Track</th></tr>"]
        for track_title, artist_name, album_title in result:
            response.extend(convert_link_strings(artist_name, album_title, track_title))
        response = "".join(response) + "</table>"
        return HttpResponse(body=response, content_type=HTML)

    else:
        return HttpResponse(body="This track isn't in the database yet!  Sorry!", content_type=HTML)


@app.get("/lyrics/<str:searchparam>")
def lyric_lookup(request, searchparam):
    searchparam = unquote(searchparam)
    response = [f"These are the tracks that have the word or phrase '{searchparam}' in its lyrics:<br />", "<table><tr><th>Artist</th><th>Album</th><th>Track</th></tr>"]

    check = database.lyric_lookup(searchparam)
    if check == db.NOT_FOUND:
        return HttpResponse(body="I couldn't find any tracks with that word/phrase in it.  Sorry!")
    for artist_name, album_title, track_title in check:
        response.extend(convert_link_strings(artist_name, album_title, track_title))
    response = "".join(response) + "</table>"
    return HttpResponse(body=response, content_type=HTML)


def convert_link_strings(artist_name, album_title, track_title):
    result = []
    track_uri = quote(track_title)
    artist_uri = quote(artist_name)
    album_uri = quote(album_title)
    result.append(f"<tr><td><a href=# onclick='$(\"#div1\").load(\"artist/{artist_uri}\")'>{artist_name}</a></td>")
    result.append(f"<td><a href=# onclick='$(\"#div1\").load(\"album/{album_uri}\")'>{album_title}</a></td>")
    result.append(f"<td><a href=# onclick='$(\"#div1\").load(\"track/{track_uri}/{artist_uri}/{album_uri}\")'>{track_title}</a></td></tr>")
    return result


if __name__ == "__main__":
    app.run(port=4000, debug=True)
