"""
This API is intended to offer administrator-only access that allows modifications to the database and doing manual runs of the scraper
"""

from os import dup
from flask import Blueprint, Response, request
from db.db_postgres import DbFunctions, NAME_COLLIDED, NOT_FOUND, NO_ITEM_TO_ADD, SUCCESS_NO_RESPONSE
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from scraper import scraper
import logging

SECRET_KEY = 

bp = Blueprint('admin', __name__, url_prefix='/admin')
database = DbFunctions()
auth = HTTPBasicAuth()
logger = logging.getLogger('api_logger')

@bp.route('', methods=['GET'])
def index():
    """
    This is a route that serves the index of /admin

    :return: Flask Response object with status code 418
    """
    return Response("This route serves a potential index page - a starting point.  It's not intended to be accessed, as I am merely a teapot.<br><br>Please read the documentation in README.md", status=418)

@auth.verify_password
def verify_password(username, password):
    """
    Simple 'HTTP Basic Authentication' check, required by all routes
    
    Checks against a complex password, which was hashed and put into 'SECRET_KEY'
    """
    if check_password_hash(SECRET_KEY, password):
        return True
    return False

@bp.route('/addartist/<string:artist>', methods=['POST'])
@auth.login_required
def add_artist(artist):
    """
    This route requires one string: the name of the artist the name of the artist to be added to the database

    :return: Flask Response object on success, or
             Flask Response object with a status code 500 on failure
    """
    artist = artist.title()
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    resp = database.add_artist(artist)
    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"{artist} added to the database!")
    else:
        return Response(f"{artist} already exists in the database!", status=500)

@bp.route('/addalbum/<string:artist>/<string:album>', methods=['POST'])
@auth.login_required
def add_album(artist, album):
    """
    This route requires two strings: the name of the artist, and the name of the album to be added to the database

    :return: Flask Response object on success, or
             Flask Response object with a status code 500 on failure
    """
    album = album.title()
    if len(artist.replace(' ', '')) < 2 or len(album.replace(' ', '')) < 2:
        return Response(f"Seems like most artists or albums should contain at least two characters!", status=500)

    resp = database.add_artist_albums(artist, [album])

    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"Added {album} for {artist} to the database!")
    elif resp == NAME_COLLIDED:
        return Response(f"The album {album} by {artist} already exists!", status=500)
    elif resp == NOT_FOUND:
        return Response(f"The artist {artist} wasn't found in the database!", status=500)

@bp.route('/addtrack/<string:artist>/<string:album>/<string:track>', methods=['POST'])
@auth.login_required
def add_track(artist, album, track):
    """
    This route requires three strings: the name of the artist, the name of the album, and the name of the track to be added to the database

    :return: Flask Response object on success, or
             Flask Response object with a status code 500 on failure
    """
    track = track.title()
    if len(artist.replace(' ', '')) < 2 or len(album.replace(' ', '')) < 2:
        return Response(f"Seems like most artists or albums should contain at least two characters!", status=500)

    dupe_check = database.view_track_lyrics(track, artist, album)
    if dupe_check[0] != NOT_FOUND:
        return Response(f"The track '{track}' on {album} by {artist} already exists!", status=500)

    resp = database.add_album_tracks(artist, album, [track])

    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"Added {track} from {album} by {artist} to the database!")
    elif resp == NOT_FOUND:
        return Response(f"The album {album} wasn't found in the database!", status=500)

@bp.route('/addlyrics/<string:artist>/<string:album>/<string:track>', methods=['POST'])
@auth.login_required
def add_lyrics(artist, album, track):
    """
    This route requires three strings: the name of the artist, the name of the album, and the name of the track to have the lyrics added to
    Also requires a JSON with the key-pair of 'lyrics': 'value of the lyrics to be added'

    :return: Flask Response object on success, or
             Flask Response object with a status code 500 on failure
    """
    if len(artist.replace(' ', '')) < 2 or len(album.replace(' ', '')) < 2:
        return Response(f"Seems like most artists or albums should contain at least two characters!", status=500)

    if 'lyrics' not in request.json:
        return Response(f"Seems like you should add some lyrics if you'd like to modify a track!  I'm checking against 'lyrics' in the JSON data", status=500)

    resp = database.add_track_lyrics(artist, album, track, request.json['lyrics'])

    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"Added lyrics to the track {track}!")
    elif resp == NOT_FOUND:
        return Response(f"The track {track} wasn't found in the database!", status=500)
    elif resp == NO_ITEM_TO_ADD:
        return Response(f"We found 'lyrics' in the JSON, but you need to specify some actual lyrics!", status=500)

@bp.route('/updateartist/<string:artist>', methods=['PUT', 'PATCH'])
@auth.login_required
def update_artist(artist):
    """
    This route requires one string: the name of the artist to be updated
    Also requires a JSON with the key-pair of 'artist': 'value of the new name for the artist'

    :return: Flask Response object on success, or
             Flask Response object with a status code 500 on failure
    """
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    if 'artist' not in request.json:
        return Response(f"You need to specify a new artist name in a JSON with the key 'artist'!", status=500)
    try:
        new_name = request.json['artist'].title()
    except AttributeError:
        return Response("You need to wrap the name in quotes!  Integers won't work", status=500)
    if len(new_name) < 2:
        return Response(f"The new artists name should also contain at least two characters!", status=500)

    dupe_check = database.view_artist_albums(new_name)
    if dupe_check != NOT_FOUND:
        return Response(f"The artist {new_name} already exists!  Please pick another name to rename the artist to.", status=500)

    resp = database.update_artist(artist, new_name)

    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"{artist} has been renamed to {new_name}")
    elif resp == NOT_FOUND:
        return Response(f"I can't find the original artist!", status=500)


@bp.route('/updatealbum/<string:artist>/<string:album>', methods=['PUT', 'PATCH'])
@auth.login_required
def update_album(artist, album):
    """
    This route requires two strings: the name of the artist, and the name of the album to be updated
    Also requires a JSON with the key-pair of 'album': 'value of the new name for the album'

    :return: Flask Response object on success, or
             Flask Response object with a status code 500 on failure
    """
    if len(artist.replace(' ', '')) < 2 or len(album.replace(' ', '')) < 2:
        return Response(f"Seems like most artists or albums should contain at least two characters!", status=500)
    if "album" not in request.json:
        return Response("You need to specify a new album name in a JSON with the key 'album'!", status=500)
    try:
        new_name = request.json['album'].title()
    except AttributeError:
        return Response("You need to wrap the name in quotes!  Integers won't work", status=500)
    if len(new_name) < 2:
        return Response(f"The new albums name should also contain at least two characters!", status=500)

    resp = database.update_album(artist, album, new_name)
    
    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"{album} has been renamed to {new_name}")
    elif resp == NAME_COLLIDED:
        return Response(f"The album {new_name} by {artist} already exists!  Please pick something unique to rename it to.", status=500)
    elif resp == NOT_FOUND:
        return Response(f"I can't find {album} by {artist}!", status=500)
    
    
@bp.route('/updatetrack/<string:artist>/<string:album>/<string:track>', methods=['PUT', 'PATCH'])
@auth.login_required
def update_track(artist, album, track):
    """
    This route requires three strings: the name of the artist, the name of the album, and the name of the track to be updated
    Also requires a JSON with the key-pair of 'track': 'value of the new name for the track'

    :return: Flask Response object on success, or
             Flask Response object with a status code 500 on failure
    """
    if len(artist.replace(' ', '')) < 2 or len(album.replace(' ', '')) < 2:
        return Response(f"Seems like most artists or albums should contain at least two characters!", status=500)
    if "track" not in request.json:
        return Response("You need to specify a new track name in a JSON with the key 'track'!", status=500)
    try:
        new_name = request.json['track'].title()
    except AttributeError:
        return Response("You need to wrap the name in quotes!  Integers won't work", status=500)
    if len(new_name) < 2:
        return Response(f"The new albums name should also contain at least two characters!", status=500)

    dupe_check = database.view_track_lyrics(new_name, artist, album)
    if dupe_check[0] != NOT_FOUND:
        return Response(f"That track '{new_name}' on {album} by {artist} already exists!", status=500)

    resp = database.update_track(artist, album, track, new_name)

    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"{track} has been renamed to {new_name}")
    elif resp == NOT_FOUND:
        return Response(f"I can't find {track} from the album {album} by {artist}!", status=500)

@bp.route('/updatelyrics/<string:artist>/<string:album>/<string:track>', methods=['PUT', 'PATCH'])
@auth.login_required
def update_lyrics(artist, album, track):
    """
    This route requires three strings: the name of the artist, the name of the album, and the name of the track to update the lyrics of
    Also requires a JSON with the key-pair of 'lyrics': 'value of the new lyrics for the track'

    :return: Flask Response object on success, or
             Flask Response object with a status code 500 on failure
    """
    if len(artist.replace(' ', '')) < 2 or len(album.replace(' ', '')) < 2:
        return Response(f"Seems like most artists or albums should contain at least two characters!", status=500)
    if 'lyrics' not in request.json:
        return Response(f"Seems like you should add some lyrics if you'd like to modify a track!  I'm checking against 'lyrics' in the json data", status=500)

    resp = database.update_lyrics(artist, album, track, request.json['lyrics'])

    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"{track} had its lyrics updated!")
    else:
        return Response(f"I can't find {track} from the album {album} by {artist}!", status=500)


@bp.route('/deleteartist/<string:artist>', methods=['DELETE'])
@auth.login_required
def delete_artist(artist):
    """
    This route requires one string: the name of the artist to be deleted
    Also requires a JSON with the key-pair of 'confirm': 'True'

    :return: Flask Response object on success, or
             Flask Response object with a status code 500 on failure
    """
    if len(artist.replace(' ', '')) < 2:
        return Response(f"Seems like most artists should contain at least two characters!", status=500)
    
    # Destructive deletes require a confirmation keyword in the JSON body
    if 'confirm' not in request.json:
        return Response("If you'd really like to delete an artist and its albums/tracks, please include 'confirm': 'True' in the JSON body.\n\nWarning, this will delete all associated albums/tracks.", status=500)
    if request.json['confirm'] != "True":
        return Response("You'll need to take the safety off - please include 'confirm': 'True' in the JSON body.\n\nWarning, this will delete all associated albums/tracks.", status=500)

    resp = database.delete_artist(artist)

    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"{artist} has been deleted!")
    else:
        return Response(f"I can't find the artist {artist}!", status=500)

@bp.route('/deletealbum/<string:artist>/<string:album>', methods=['DELETE'])
@auth.login_required
def delete_album(artist, album):
    """
    This route requires two strings: the name of the artist, and the name of the album to be deleted
    Also requires a JSON with the key-pair of 'confirm': 'True'

    :return: Flask Response object on success, or
             Flask Response object with a status code 500 on failure
    """
    if len(artist.replace(' ', '')) < 2 or len(album.replace(' ', '')) < 2:
        return Response(f"Seems like most artists or albums should contain at least two characters!", status=500)

    # Destructive deletes require a confirmation keyword in the JSON body
    if 'confirm' not in request.json:
        return Response("If you'd really like to delete a whole album and its tracks, please include 'confirm': 'True' in the JSON body.\n\nWarning, this will delete all associated tracks.")
    if request.json['confirm'] != "True":
        return Response("You'll need to take the safety off - please include 'confirm': 'True' in the JSON body.\n\nWarning, this will delete all associated tracks.")

    resp = database.delete_album(artist, album)

    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"{album} has been deleted!")
    else:
        return Response(f"I can't find the album {album} by {artist}!", status=500)

@bp.route('/deletetrack/<string:artist>/<string:album>/<string:track>', methods=['DELETE'])
@auth.login_required
def delete_track(artist, album, track):
    """
    This route requires three strings: the name of the artist, the name of the album, and the name of the track to be deleted
    Also requires a JSON with the key-pair of 'confirm': 'True'

    :return: Flask Response object on success, or
             Flask Response object with a status code 500 on failure
    """
    if len(artist.replace(' ', '')) < 2 or len(album.replace(' ', '')) < 2:
        return Response(f"Seems like most artists or albums should contain at least two characters!", status=500)
    
    # Destructive deletes require a confirmation keyword in the JSON body
    if 'confirm' not in request.json:
        return Response("If you'd really like to delete this track, please include 'confirm': True in the JSON body.")
    if request.json['confirm'] != "True":
        return Response("You'll need to take the safety off - please include 'confirm': 'True' in the JSON body.")


    resp = database.delete_track(artist, album, track)

    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"{track} has been deleted!")
    else:
        return Response(f"I can't find {track} from the album {album} by {artist}!", status=500)

@bp.route('/deletelyrics/<string:artist>/<string:album>/<string:track>', methods=['DELETE'])
@auth.login_required
def delete_lyrics(artist, album, track):
    """
    This route requires three strings: the name of the artist, the name of the album, and the name of the track to have the lyrics deleted from
    Also requires a JSON with the key-pair of 'confirm': 'True'

    :return: Flask Response object on success, or
             Flask Response object with a status code 500 on failure
    """
    if len(artist.replace(' ', '')) < 2 or len(album.replace(' ', '')) < 2:
        return Response(f"Seems like most artists or albums should contain at least two characters!", status=500)
    
    # Destructive deletes require a confirmation keyword in the JSON body
    if 'confirm' not in request.json:
        return Response("If you'd really like to delete this track, please include 'confirm': True in the JSON body.")
    if request.json['confirm'] != "True":
        return Response("You'll need to take the safety off - please include 'confirm': 'True' in the JSON body.")

    resp = database.delete_lyrics(artist, album, track)

    if resp == SUCCESS_NO_RESPONSE:
        return Response(f"{track} had its lyrics emptied!")
    else:
        return Response(f"I can't find {track} from the album {album} by {artist}!", status=500)

@bp.route('/scrapeartists', methods=['GET'])
@auth.login_required
def scrape_artists():
    """
    This route requires a JSON with the key-pair related to the intended action:
        'full_run': 'True' for a full run of unparsed artists
        'artists': ['list of artists'] for specific artists

    :return: Flask Response object on scraper completion, or
             Flask Response object with a status code 500 on no valid JSON tags present
    """
    artists_to_scrape = []

    if 'full_run' in request.json:
        if request.json['full_run'] == 'True':
            logger.error("Manual full artist run initiated")
            scraper.get_albums()
            return Response("Manual full artist scraper run complete!")
    if 'artists' in request.json:
        for i, artist in enumerate(request.json['artists']):
            if len(artist) == 1 and i == 0:
                artists_to_scrape = [request.json['artists']]
                break
            else:
                artists_to_scrape.append(artist)
        scraper.get_albums(artists_to_scrape)
        return Response(f"Manual artists scraper run complete with the following artists:<br>{'<br>'.join(artists_to_scrape)}")
        
    return Response("Please use the JSON body to define what you'd like to scrape.  Check the docs for more info.", status=500)

@bp.route('/scrapealbums', methods=['GET'])
@auth.login_required
def scrape_albums():
    """
    This route requires a JSON with the key-pair related to the intended action:
        'full_run': 'True' for a full run of unparsed albums
        'album': {'example_artist': 'example_album'} for specific artist/album combinations

    :return: Flask Response object on scraper completion, or
             Flask Response object with a status code 500 on no valid JSON tags present
    """
    albums_to_scrape = []

    if 'full_run' in request.json:
        if request.json['full_run'] == 'True':
            logger.error("Manual full album run initiated")
            scraper.get_tracks()
            return Response("Manual full album scraper run complete!")
    if 'albums' in request.json:
        for album_set in request.json['albums'].items():
            albums_to_scrape.append(f"{album_set[0]}'s album {album_set[1]}")
            scraper.get_tracks(album_set[0], album_set[1])
        return Response(f"Manual album scraper run complete with the following artist/album combinations:<br>{'<br>'.join(albums_to_scrape)}")
        
    return Response("Please use the JSON body to define what you'd like to scrape.  Check the docs for more info.", status=500)

@bp.route('/scrapetracks', methods=['GET'])
@auth.login_required
def scrape_tracks():
    """
    This route requires a JSON with the key-pair related to the intended action:
        'full_run': 'True' for a full run of unparsed tracks
        'second_run': 'True' for a full run of parsed tracks that still have 'NULL' as their lyrics
        'album': [['artist', 'album', 'track']] for specific artist/album combinations

    :return: Flask Response object on scraper completion, or
             Flask Response object with a status code 500 on no valid JSON tags present
    """
    tracks_to_scrape = []

    if 'full_run' in request.json:
        if request.json['full_run'] == 'True':
            logger.error("Manual full track/lyric run initiated")
            scraper.get_lyrics()
            return Response("Manual full track/lyric run complete!")
    if 'second_pass' in request.json:
        if request.json['second_pass'] == 'True':
            logger.error("Second pass manual run initiated")
            scraper.second_pass_lyrics()
            return Response("Manual second pass lyric scraper run complete!")
    if 'tracks' in request.json:
        print(request.json['tracks'])
        for request_set in request.json['tracks']:
            tracks_to_scrape.append(f"{request_set[2]} from {request_set[0]}'s album {request_set[1]}")
            scraper.get_lyrics(request_set[0], request_set[1], request_set[2])
        return Response(f"Manual lyric scraper run complete with the following tracks:<br>{'<br>'.join(tracks_to_scrape)}")
    return Response("Please use the JSON body to define what you'd like to scrape.  Check the docs for more info.", status=500)
