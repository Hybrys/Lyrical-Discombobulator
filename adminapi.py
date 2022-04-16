"""
This API is intended to fill the requirements for the Portfolio Project for NuCamp Spring 2022

THIS API IS NOT INTENDED TO GO LIVE AND SHOULD NOT BE DEPLOYED AS IT IS POTENTIALLY AND INTENTIONALLY DESTRUCTIVE
"""
import os
os.environ["DATABASE"] = "test"

from flask import Blueprint, Response, request
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session
from db.db_postgres import *

bp = Blueprint('admin', __name__, url_prefix='/admin')

def dbinit():
    engine = create_engine("postgresql+pg8000://postgres:@localhost:5454/postgres").execution_options(isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        conn.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'test'
            AND pid <> pg_backend_pid();
        """)
        conn.execute("DROP DATABASE IF EXISTS test")
        conn.execute("CREATE DATABASE test")
    engine.dispose()

    engine = create_engine("postgresql+pg8000://postgres:@localhost:5454/test")
    db = Session(engine)
    db.execute("CREATE TABLE IF NOT EXISTS artists (artist_id SERIAL PRIMARY KEY, name TEXT, isparsed BOOLEAN, UNIQUE(name))")
    db.execute("CREATE TABLE IF NOT EXISTS albums (album_id SERIAL PRIMARY KEY, album_title TEXT, artist_id INTEGER, isparsed BOOLEAN, FOREIGN KEY(artist_id) REFERENCES artists(artist_id), UNIQUE(album_title, artist_id))")
    db.execute("CREATE TABLE IF NOT EXISTS tracks (track_id SERIAL PRIMARY KEY, track_title TEXT, track_num INTEGER, lyrics TEXT, album_id INTEGER, parse_tried BOOLEAN, FOREIGN KEY(album_id) REFERENCES albums(album_id), UNIQUE(track_title, album_id))")
    db.commit()
    db.close()
    engine.dispose()

@bp.route('', methods=['GET'])
def index():
    return Response("This route serves a potential index page - a starting point.  It's not intended to be accessed, as I am merely a teapot.  Please read the documentation in api.md", status=418)

@bp.route('/addartist/<string:artist>', methods=['POST'])
def add_artist(artist):
    artist = artist.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    database = DbFunctions()
    resp = database.add_artist(artist)
    database.close()
    return Response(f"{artist} added to the database!")

@bp.route('/addalbum/<string:artist>/<string:album>', methods=['POST'])
def add_album(artist, album):
    artist = artist.title()
    album = album.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    if len(album.replace(' ', '')) < 2:
        return Response(f"Seems like this album should have at least two characters in it!", status=500)
    database = DbFunctions()
    resp = database.add_artist_albums(artist, [album])
    database.close()
    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"Added {album} for {artist} to the database!")
    elif resp == NOT_FOUND:
        return Response(f"The artist {artist} wasn't found in the database!  It needs to exist before we can add albums to it!", status=500)

@bp.route('/addtrack/<string:artist>/<string:album>/<string:track>', methods=['POST'])
def add_track(artist, album, track):
    artist = artist.title()
    album = album.title()
    track = track.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    if len(album.replace(' ', '')) < 2:
        return Response(f"Seems like this album should have at least two characters in it!", status=500)
    database = DbFunctions()
    resp = database.add_album_tracks(artist, album, [track])
    database.close()
    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"Added {track} from {album} by {artist} to the database!")
    elif resp == NOT_FOUND:
        return Response(f"The album {album} wasn't found in the database!  It needs to exist before we can add tracks to it!", status=500)

@bp.route('/addlyrics/<string:artist>/<string:album>/<string:track>', methods=['POST'])
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
    database = DbFunctions()
    resp = database.add_track_lyrics(artist, album, track, request.json['lyrics'])
    database.close()
    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"Added lyrics to the track {track}!")
    elif resp == NOT_FOUND:
        return Response(f"The track {track} wasn't found in the database!  It needs to exist before we can add lyrics to it!", status=500)
    elif resp == NO_ITEM_TO_ADD:
        return Response(f"We found 'lyrics' in the JSON, but you need to specify some actual lyrics!", status=500)

@bp.route('/updateartist/<string:artist>', methods=['PUT', 'PATCH'])
def update_artist(artist):
    artist = artist.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    if 'artist' not in request.json:
        return Response(f"You need to specify a new artist name in a JSON with the key 'artist'!", status=500)
    if len(request.json['artist']) < 2:
        return Response(f"The new artists name should also contain at least two characters!", status=500)

    engine = create_engine("postgresql+pg8000://postgres:@localhost:5454/test").execution_options(autocommit=True)
    database = Session(engine)
    check = database.execute(text("SELECT * FROM artists WHERE name = :artist"), {"artist": artist}).fetchone()
    if check == None:
        database.close()
        engine.dispose()
        return Response(f"I can't find the original artist!", status=500)
    else:
        database.execute(text("UPDATE artists SET name = :artistjson WHERE name = :artist"), {"artistjson": request.json["artist"], "artist": artist})
        database.commit()
        database.close()
        engine.dispose()
        return Response(f"{artist} has been renamed to {request.json['artist']}")
    

@bp.route('/updatealbum/<string:artist>/<string:album>', methods=['PUT', 'PATCH'])
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

    engine = create_engine("postgresql+pg8000://postgres:@localhost:5454/test").execution_options(autocommit=True)
    database = Session(engine)
    check = database.execute(text("SELECT albums.artist_id, artists.name, albums.album_title FROM albums JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name = :artist AND albums.album_title = :album"), {"artist": artist, "album": album}).fetchone()
    if check == None:
        database.close()
        engine.dispose()
        return Response(f"I can't find the original album!", status=500)
    else:
        database.execute(text("UPDATE albums SET album_title = :albumjson WHERE album_title = :album AND artist_id = :artist_id"), {"albumjson": request.json["album"], "album": album, "artist_id": check[0]})
        database.commit()
        database.close()
        engine.dispose()
        return Response(f"{album} has been renamed {request.json['album']}")
    
    
@bp.route('/updatetrack/<string:artist>/<string:album>/<string:track>', methods=['PUT', 'PATCH'])
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

    engine = create_engine("postgresql+pg8000://postgres:@localhost:5454/test").execution_options(autocommit=True)
    database = Session(engine)
    check = database.execute(text("SELECT tracks.album_id, tracks.track_title, artists.name, albums.album_title FROM tracks JOIN albums ON tracks.album_ID = albums.album_id JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name = :artist AND albums.album_title = :album and tracks.track_title = :track"), {"artist": artist, "album": album, "track": track}).fetchone()
    if check == None:
        database.close()
        engine.dispose()
        return Response(f"I can't find that track!", status=500)
    else:
        database.execute(text("UPDATE tracks SET track_title = :trackjson WHERE track_title = :track AND album_id = :album_id"), {"trackjson": request.json["track"], "track": track, "album_id": check[0]})
        database.commit()
        database.close()
        engine.dispose()
        return Response(f"{track} has been renamed to {request.json['track']}")

@bp.route('/updatelyrics/<string:artist>/<string:album>/<string:track>', methods=['PUT', 'PATCH'])
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
    engine = create_engine("postgresql+pg8000://postgres:@localhost:5454/test").execution_options(autocommit=True)
    database = Session(engine)
    check = database.execute(text("SELECT tracks.album_id, tracks.track_title, artists.name, albums.album_title FROM tracks JOIN albums ON tracks.album_ID = albums.album_id JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name = :artist AND albums.album_title = :album and tracks.track_title = :track"), {"artist": artist, "album": album, "track": track}).fetchone()
    if check == None:
        database.close()
        engine.dispose()
        return Response(f"I can't find that track!", status=500)
    else:
        database.execute(text("UPDATE tracks SET lyrics = :lyricsjson WHERE track_title = :track AND album_id = :album_id"), {"lyricsjson": request.json["lyrics"], "track": track, "album_id": check[0]})
        database.commit()
        database.close()
        engine.dispose()
        return Response(f"{track} had its lyrics updated!")
    

@bp.route('/deletetrack/<string:artist>/<string:album>/<string:track>', methods=['DELETE'])
def remove_track(artist, album, track):
    artist = artist.title()
    album = album.title()
    track = track.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    if len(album.replace(' ', '')) < 2:
        return Response(f"Seems like this album should have at least two characters in it!", status=500)
    engine = create_engine("postgresql+pg8000://postgres:@localhost:5454/test").execution_options(autocommit=True)
    database = Session(engine)
    check = database.execute(text("SELECT tracks.album_id, tracks.track_title, artists.name, albums.album_title FROM tracks JOIN albums ON tracks.album_ID = albums.album_id JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name = :artist AND albums.album_title = :album and tracks.track_title = :track"), {"artist": artist, "album": album, "track": track}).fetchone()
    if check == None:
        database.close()
        engine.dispose()
        return Response(f"I can't find that track!", status=500)
    else:
        database.execute(text("DELETE FROM tracks WHERE track_title = :track AND album_id = :album_id"), {"track": track, "album_id": check[0]})
        database.commit()
        database.close()
        engine.dispose()
        return Response(f"{track} deleted!")