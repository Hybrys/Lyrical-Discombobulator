"""
This API is intended to be an administrator-only API that allows for adding to the database and doing manual runs of the scraper without needing to modify the code
"""
from flask import Blueprint, Response, request
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session
from db.db_postgres import *
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

SECRET_KEY = "pbkdf2:sha256:260000$PAGsZbqZr7kmjlik$d14d560e9395142b4068facac3266805532b92c5441306fbbd20b1d0ffd7ecd2"

bp = Blueprint('admin', __name__, url_prefix='/admin')
database = DbFunctions()
auth = HTTPBasicAuth()

@bp.route('', methods=['GET'])
def index():
    return Response("This route serves a potential index page - a starting point.  It's not intended to be accessed, as I am merely a teapot.  Please read the documentation in README.md", status=418)

@auth.verify_password
def verify_password(username, password):
    if check_password_hash(SECRET_KEY, password):
        return True
    return False

@bp.route('/addartist/<string:artist>', methods=['POST'])
@auth.login_required
def add_artist(artist):
    artist = artist.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    resp = database.add_artist(artist)
    return Response(f"{artist} added to the database!")

@bp.route('/addalbum/<string:artist>/<string:album>', methods=['POST'])
@auth.login_required
def add_album(artist, album):
    artist = artist.title()
    album = album.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    if len(album.replace(' ', '')) < 2:
        return Response(f"Seems like this album should have at least two characters in it!", status=500)
    resp = database.add_artist_albums(artist, [album])
    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"Added {album} for {artist} to the database!")
    elif resp == NOT_FOUND:
        return Response(f"The artist {artist} wasn't found in the database!  It needs to exist before we can add albums to it!", status=500)

@bp.route('/addtrack/<string:artist>/<string:album>/<string:track>', methods=['POST'])
@auth.login_required
def add_track(artist, album, track):
    artist = artist.title()
    album = album.title()
    track = track.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    if len(album.replace(' ', '')) < 2:
        return Response(f"Seems like this album should have at least two characters in it!", status=500)
    resp = database.add_album_tracks(artist, album, [track])
    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"Added {track} from {album} by {artist} to the database!")
    elif resp == NOT_FOUND:
        return Response(f"The album {album} wasn't found in the database!  It needs to exist before we can add tracks to it!", status=500)

@bp.route('/addlyrics/<string:artist>/<string:album>/<string:track>', methods=['POST'])
@auth.login_required
def add_lyrics(artist, album, track):
    artist = artist.title()
    album = album.title()
    track = track.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    if len(album.replace(' ', '')) < 2:
        return Response(f"Seems like this album should have at least two characters in it!", status=500)
    if 'lyrics' not in request.json:
        return Response(f"Seems like you should add some lyrics if you'd like to modify a track!  I'm checking against lyrics in the json data", status=500)
    resp = database.add_track_lyrics(artist, album, track, request.json['lyrics'])
    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"Added lyrics to the track {track}!")
    elif resp == NOT_FOUND:
        return Response(f"The track {track} wasn't found in the database!  It needs to exist before we can add lyrics to it!", status=500)
    elif resp == NO_ITEM_TO_ADD:
        return Response(f"We found 'lyrics' in the JSON, but you need to specify some actual lyrics!", status=500)

@bp.route('/updateartist/<string:artist>', methods=['PUT', 'PATCH'])
@auth.login_required
def update_artist(artist):
    artist = artist.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    if 'artist' not in request.json:
        return Response(f"You need to specify a new artist name in a JSON with the key 'artist'!", status=500)
    if len(request.json['artist']) < 2:
        return Response(f"The new artists name should also contain at least two characters!", status=500)

    # engine = create_engine("postgresql+pg8000://postgres:@localhost:5454/test").execution_options(autocommit=True)
    # database = Session(engine)
    # check = database.execute(text("SELECT * FROM artists WHERE name = :artist"), {"artist": artist}).fetchone()
    # if check == None:
    #     database.close()
    #     engine.dispose()
    #     return Response(f"I can't find the original artist!", status=500)
    # else:
    #     database.execute(text("UPDATE artists SET name = :artistjson WHERE name = :artist"), {"artistjson": request.json["artist"], "artist": artist})
    #     database.commit()
    #     database.close()
    #     engine.dispose()
    #     return Response(f"{artist} has been renamed to {request.json['artist']}")
    

@bp.route('/updatealbum/<string:artist>/<string:album>', methods=['PUT', 'PATCH'])
@auth.login_required
def update_album(artist, album):
    artist = artist.title()
    album = album.title()
    if len(artist.replace(' ', '')) < 2:
        return Response("Seems like most artists should contain at least two characters!", status=500)
    if len(album.replace(' ', '')) < 2:
        return Response("Seems like this album should have at least two characters in it!", status=500)
    if "album" not in request.json:
        return Response("You need to specify a new album name in a JSON with the key 'album'!", status=500)
    if len(request.json['album']) < 2:
        return Response(f"The new albums name should also contain at least two characters!", status=500)

    # engine = create_engine("postgresql+pg8000://postgres:@localhost:5454/test").execution_options(autocommit=True)
    # database = Session(engine)
    # check = database.execute(text("SELECT albums.artist_id, artists.name, albums.album_title FROM albums JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name = :artist AND albums.album_title = :album"), {"artist": artist, "album": album}).fetchone()
    # if check == None:
    #     database.close()
    #     engine.dispose()
    #     return Response(f"I can't find the original album!", status=500)
    # else:
    #     database.execute(text("UPDATE albums SET album_title = :albumjson WHERE album_title = :album AND artist_id = :artist_id"), {"albumjson": request.json["album"], "album": album, "artist_id": check[0]})
    #     database.commit()
    #     database.close()
    #     engine.dispose()
    #     return Response(f"{album} has been renamed {request.json['album']}")
    
    
@bp.route('/updatetrack/<string:artist>/<string:album>/<string:track>', methods=['PUT', 'PATCH'])
@auth.login_required
def update_track(artist, album, track):
    artist = artist.title()
    album = album.title()
    track = track.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    if len(album.replace(' ', '')) < 2:
        return Response(f"Seems like this album should have at least two characters in it!", status=500)
    if "track" not in request.json:
        return Response("You need to specify a new track name in a JSON with the key 'track'!", status=500)
    if len(request.json['track']) < 1:
        return Response(f"The new tracks name should also contain at least one characters!", status=500)

    # engine = create_engine("postgresql+pg8000://postgres:@localhost:5454/test").execution_options(autocommit=True)
    # database = Session(engine)
    # check = database.execute(text("SELECT tracks.album_id, tracks.track_title, artists.name, albums.album_title FROM tracks JOIN albums ON tracks.album_ID = albums.album_id JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name = :artist AND albums.album_title = :album and tracks.track_title = :track"), {"artist": artist, "album": album, "track": track}).fetchone()
    # if check == None:
    #     database.close()
    #     engine.dispose()
    #     return Response(f"I can't find that track!", status=500)
    # else:
    #     database.execute(text("UPDATE tracks SET track_title = :trackjson WHERE track_title = :track AND album_id = :album_id"), {"trackjson": request.json["track"], "track": track, "album_id": check[0]})
    #     database.commit()
    #     database.close()
    #     engine.dispose()
    #     return Response(f"{track} has been renamed to {request.json['track']}")

@bp.route('/updatelyrics/<string:artist>/<string:album>/<string:track>', methods=['PUT', 'PATCH'])
@auth.login_required
def update_lyrics(artist, album, track):
    artist = artist.title()
    album = album.title()
    track = track.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    if len(album.replace(' ', '')) < 2:
        return Response(f"Seems like this album should have at least two characters in it!", status=500)
    if 'lyrics' not in request.json:
        return Response(f"Seems like you should add some lyrics if you'd like to modify a track!  I'm checking against 'lyrics' in the json data")

    # engine = create_engine("postgresql+pg8000://postgres:@localhost:5454/test").execution_options(autocommit=True)
    # database = Session(engine)
    # check = database.execute(text("SELECT tracks.album_id, tracks.track_title, artists.name, albums.album_title FROM tracks JOIN albums ON tracks.album_ID = albums.album_id JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name = :artist AND albums.album_title = :album and tracks.track_title = :track"), {"artist": artist, "album": album, "track": track}).fetchone()
    # if check == None:
    #     database.close()
    #     engine.dispose()
    #     return Response(f"I can't find that track!", status=500)
    # else:
    #     database.execute(text("UPDATE tracks SET lyrics = :lyricsjson WHERE track_title = :track AND album_id = :album_id"), {"lyricsjson": request.json["lyrics"], "track": track, "album_id": check[0]})
    #     database.commit()
    #     database.close()
    #     engine.dispose()
    #     return Response(f"{track} had its lyrics updated!")
    

@bp.route('/deletetrack/<string:artist>/<string:album>/<string:track>', methods=['DELETE'])
@auth.login_required
def remove_track(artist, album, track):
    artist = artist.title()
    album = album.title()
    track = track.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    if len(album.replace(' ', '')) < 2:
        return Response(f"Seems like this album should have at least two characters in it!", status=500)
    
    # engine = create_engine("postgresql+pg8000://postgres:@localhost:5454/test").execution_options(autocommit=True)
    # database = Session(engine)
    # check = database.execute(text("SELECT tracks.album_id, tracks.track_title, artists.name, albums.album_title FROM tracks JOIN albums ON tracks.album_ID = albums.album_id JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name = :artist AND albums.album_title = :album and tracks.track_title = :track"), {"artist": artist, "album": album, "track": track}).fetchone()
    # if check == None:
    #     database.close()
    #     engine.dispose()
    #     return Response(f"I can't find that track!", status=500)
    # else:
    #     database.execute(text("DELETE FROM tracks WHERE track_title = :track AND album_id = :album_id"), {"track": track, "album_id": check[0]})
    #     database.commit()
    #     database.close()
    #     engine.dispose()
    #     return Response(f"{track} deleted!")