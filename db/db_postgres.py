"""
Postgresql database interaction handler for the scraper and frontend systems, as a class
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from os import environ

NOT_FOUND = 0
NAME_COLLIDED = 1
NO_ITEM_TO_ADD = 2
SUCCESS_NO_RESPONSE = 3
MANY_FOUND = 4
NO_CONTENT = 5

class DbFunctions():
    def __init__(self):
        """
        Initialize the database for use - create the tables and file if it doesn't exist.

        :param filename: Optional param for using a test database
        """
        # Check env variables for db
        db_name = environ.get('DATABASE')
        db_user = environ.get('DB_USER')
        db_pass = environ.get('DB_PASS')
        db_location = environ.get('DB_LOC')

        # Find out if I'm containerized
        container_check = environ.get('CONTAINER_DB')
        if container_check == "":
            db_location = "localhost:5454"
        engine_uri = f"postgresql+pg8000://{db_user}:{db_pass}@{db_location}/{db_name}"
        
        unix_socket = environ.get('DB_UNIX')
        if unix_socket != "":
            engine_uri = f"postgresql+pg8000://{db_user}:{db_pass}@/{db_name}?unix_sock={db_location}"

        self.database = create_engine(engine_uri)

        with Session(self.database) as db:
            db.execute("CREATE TABLE IF NOT EXISTS artists (artist_id SERIAL PRIMARY KEY, name TEXT, isparsed BOOLEAN, UNIQUE(name))")
            db.execute("CREATE TABLE IF NOT EXISTS albums (album_id SERIAL PRIMARY KEY, album_title TEXT, artist_id INTEGER, isparsed BOOLEAN, FOREIGN KEY(artist_id) REFERENCES artists(artist_id), UNIQUE(album_title, artist_id))")
            db.execute("CREATE TABLE IF NOT EXISTS tracks (track_id SERIAL PRIMARY KEY, track_title TEXT, track_num INTEGER, lyrics TEXT, album_id INTEGER, parse_tried BOOLEAN, FOREIGN KEY(album_id) REFERENCES albums(album_id), UNIQUE(track_title, album_id))")
            db.commit()

    def add_artist(self, artist):
        """
        Adds one single artist to the database

        :param artist: The name of the artist to add as a string
        :return: SUCCESS_NO_RESPONSE if successful, or
                 NAME_COLLIDED if the artist already exists in the database
        """
        with Session(self.database) as db:
            name_test = db.execute("SELECT * FROM artists WHERE name ILIKE :name", {"name": artist}).fetchone()
        if name_test == None:
            with Session(self.database) as db:
                db.execute("INSERT INTO artists (name, isparsed) VALUES (:artist, :isparsed)", {"artist": artist, "isparsed": False})
                db.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NAME_COLLIDED

    def add_artist_albums(self, artist, albums):
        """
        Adds an artists albums to the albums database with a reference to the artist name to fetch the artist_id primary/foreign key

        :param artist: Artist name as a string
        :param albums: Album names as a list
        :return: SUCCESS_NO_RESPONSE if successful, or
                 NO_ITEM_TO_ADD if the list of albums is empty
        """
        duplicate_found = 0

        if albums == None or albums == []:
            return NO_ITEM_TO_ADD

        with Session(self.database) as db:
            artist_id = db.execute("SELECT artist_id FROM artists WHERE name = :name", {"name": artist}).fetchone()
        if artist_id == None:
            return NOT_FOUND

        with Session(self.database) as db:    
            for album in albums:
                dupe_check = db.execute("SELECT * FROM albums WHERE artist_id = :artist_id AND album_title = :album_title", {"artist_id": artist_id[0], "album_title": album}).fetchone()
                if dupe_check == None:
                    db.execute("INSERT INTO albums (album_title, artist_id, isparsed) VALUES (:album, :artist_id, :isparsed)", {"album": album, "artist_id": artist_id[0], "isparsed": False})
                else:
                    duplicate_found = 1
            db.execute("UPDATE artists SET isparsed = :isparsed WHERE artist_id = :artist_id", {"isparsed": True, "artist_id": artist_id[0]})
            db.commit()
        if duplicate_found != 0:
            return NAME_COLLIDED
        return SUCCESS_NO_RESPONSE


    def add_album_tracks(self, artist, album, tracks):
        """
        Add tracks to the 'tracks' database, referencing the album name to fetch the album_id primary/foreign key

        :param artist: The artist name as a string
        :param album: The album name as a string
        :param tracks: The tracks as a list
        :return: SUCCESS_NO_RESPONSE if successful, or
                 NOT_FOUND if it cannot find a match between artist and album, or
                 NO_ITEM_TO_ADD if the list of tracks is empty
        """
        album_id = self.album_artist_match(artist, album)
        if album_id == NOT_FOUND:
            return NOT_FOUND

        if tracks != None and tracks != []:
            with Session(self.database) as db:
                for index, track in enumerate(tracks):
                    db.execute("INSERT INTO tracks (track_title, track_num, album_id) VALUES (:track_title, :track_num, :album_id) ON CONFLICT DO NOTHING", {"track_title": track, "track_num": index+1, "album_id": album_id})
                db.execute("UPDATE albums SET isparsed = :isparsed WHERE album_id = :album_id", {"isparsed": True, "album_id": album_id})
                db.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NO_ITEM_TO_ADD

    def add_track_lyrics(self, artist, album, track, lyrics):
        """
        Add lyrics to the 'tracks' database, referencing the track name

        :param artist: The artist name as a string
        :param album: The album name as a string
        :param track: The track name as a string
        :return: SUCCESS_NO_RESPONSE if successful, or
                 NOT_FOUND if it cannot find a match between artist and album, or track name and album id, or
                 NO_ITEM_TO_ADD if the track string is empty
        """
        album_id = self.album_artist_match(artist, album)
        if album_id == NOT_FOUND:
            return NOT_FOUND
        
        with Session(self.database) as db:
            track_check = db.execute("SELECT track_id FROM tracks WHERE track_title ILIKE :track_title AND album_id = :album_id", {"track_title": f"%{track}%", "album_id": album_id}).fetchone()
        if track_check == None:
            return NOT_FOUND

        if lyrics != None and lyrics != "":
                with Session(self.database) as db:
                    db.execute("UPDATE tracks SET lyrics = :lyrics, parse_tried = :parse_tried WHERE track_id = :track_id AND album_id = :album_id", {"lyrics": lyrics, "parse_tried": True, "track_id": track_check[0], "album_id": album_id})
                    db.commit()
                return SUCCESS_NO_RESPONSE
        else:
            with Session(self.database) as db:
                db.execute("UPDATE tracks SET parse_tried = :parse_tried WHERE track_id = :track_id AND album_id = :album_id",  {"parse_tried": True, "track_id": track_check[0], "album_id": album_id})
                db.commit()
            return NO_ITEM_TO_ADD

    def album_artist_match(self, artist, album):
        """
        Artist to album matching for cases in which the album title matches against more than one album

        :param artist: The name of the artist to match the ID of
        :param album: The name of the album to match the name of
        :returns: An integer of the artist ID of the first match between album name and artist name, or
                  NOT_FOUND if a match cannot be found
        """
        with Session(self.database) as db:
            album_name_matches = db.execute("SELECT artist_id, album_id FROM albums WHERE album_title ILIKE :album_title", {"album_title": f"%{album}%"}).fetchall()
        for match in album_name_matches:
            with Session(self.database) as db:
                artist_check = db.execute("SELECT name FROM artists WHERE artist_id = :artist_id", {"artist_id": match[0]}).fetchone()
            if artist_check[0].lower() == artist.lower():
                return match[1]
            else:
                continue
        return NOT_FOUND

    def view_unparsed_artists(self):
        """
        View all artists that are not yet parsed

        :return: A list of the artists that have a False for the isparsed flag
        """
        result = []
        with Session(self.database) as db:
            artists = db.execute("SELECT name FROM artists WHERE isparsed = :isparsed", {"isparsed": False}).fetchall()
        for artist in artists:
            result.append(artist[0])
        return result

    def view_unparsed_albums(self):
        """
        View all albums that are not yet parsed, with a False for the isparsed flag

        :return: A list of lists for each artist, with each list containing the album and artist name
        """
        result = []
        with Session(self.database) as db:
            unparsed_albums = db.execute("SELECT album_title, artist_id FROM albums WHERE isparsed = :isparsed", {"isparsed": False}).fetchall()
        for album in unparsed_albums:
            with Session(self.database) as db:
                artist_name = db.execute("SELECT name FROM artists WHERE artist_id = :artist_id", {"artist_id": album[1]}).fetchone()
            result.append([artist_name[0], album[0]])
        return result

    # Checks for first pass missed tracks
    # New variable 'parse_tried' in the tracks table will let us check second pass tracks
    def view_unparsed_tracks(self):
        """
        View all tracks that have an empty lyrics field and an empty parse_tried flag

        :return: A list of lists where each list contains the artist name, album title, and track title
        """
        result = []
        with Session(self.database) as db:
            unparsed_tracks = db.execute("SELECT track_title, album_id FROM tracks WHERE lyrics IS NULL AND parse_tried IS NULL").fetchall()
        for track in unparsed_tracks:
            with Session(self.database) as db:
                album_info = db.execute("SELECT album_title, artist_id FROM albums WHERE album_id = :album_id", {"album_id": track[1]}).fetchone()
                artist_name = db.execute("SELECT name FROM artists WHERE artist_id = :artist_id", {"artist_id": album_info[1]}).fetchone()
            result.append([artist_name[0], album_info[0], track[0]])
        return result

    # Checks for first pass missed tracks
    def second_pass_empty_tracks(self):
        """
        View all tracks that still contain no lyrics after the first pass, where the lyrics field remains empty but 'parse_tried' is True

        :return: A list of lists for each artist that have a False for the isparsed flag, with each list containing the artist name, album title, track title, and the album_id
        """
        result = []
        with Session(self.database) as db:
            unparsed_tracks = db.execute("SELECT track_title, album_id FROM tracks WHERE lyrics IS NULL AND parse_tried = :parse_tried", {"parse_tried": True}).fetchall()
        for track in unparsed_tracks:
            with Session(self.database) as db:
                album_info = db.execute("SELECT album_title, artist_id FROM albums WHERE album_id = :album_id", {"album_id": track[1]}).fetchone()
                artist_name = db.execute("SELECT name FROM artists WHERE artist_id = :artist_id", {"artist_id": album_info[1]}).fetchone()
            result.append([artist_name[0], album_info[0], track[0]])
        return result

    def view_artist_albums(self, artist):
        """
        View all of an artists albums

        :param artist: Artist name as a string
        :return: A list of lists, with each list containing the artist name and one album, or 
                 NOT_FOUND if the artist cannot be found, or
                 NO_CONTENT if the artist is found but has no albums in the database.
        """
        result = []
        with Session(self.database) as db:
            artist_id = db.execute("SELECT name, artist_id FROM artists WHERE name ILIKE :name", {"name": artist}).fetchone()
        if artist_id == None:
            return NOT_FOUND
        with Session(self.database) as db:
            dbresult = db.execute("SELECT album_title FROM albums WHERE artist_id = :artistid", {"artistid": artist_id[1]}).fetchall()
        if dbresult == []:
            return NO_CONTENT
        for res in dbresult:
            result.append([artist_id[0], res[0]])
        return result

    def view_artist_albums_fuzzy(self, artist):
        """
        View all of an artists albums matching closest to the searched terms

        :param artist: Artist name as a string
        :return: Returns a list of potential artist matches, or
                 NOT_FOUND if it cannot find any matches to the LIKE query
        """
        result = []
        with Session(self.database) as db:
            artist_list = db.execute("SELECT name, artist_id FROM artists WHERE name ILIKE :name_seg", {"name_seg": f"%{artist}%"}).fetchall()
        if artist_list == []:
            return NOT_FOUND
        else:
            for artist in artist_list:
                result.append([artist[0]])
        return result

    def view_album_tracks(self, album):
        """
        View all of an albums tracks

        :param artist: Album name as a string
        :return: A list of the tracks from that album, or
                 NOT_FOUND if the album cannot be found, or
                 NO_CONTENT if the album has no tracks associated with it in the database.
        """
        result = []
        with Session(self.database) as db:
            album_id = db.execute("SELECT album_id, name, album_title FROM albums JOIN artists ON albums.artist_id = artists.artist_id WHERE album_title ILIKE :album_title", {"album_title": album}).fetchone()
        if album_id == None:
            return NOT_FOUND
        with Session(self.database) as db:
            tracks = db.execute("SELECT track_title FROM tracks WHERE album_id = :album_id", {"album_id": album_id[0]}).fetchall()
        if tracks == []:
            return NO_CONTENT
        for track in tracks:
            result.append([album_id[1], album_id[2], track[0]])
        return result

    def view_album_tracks_fuzzy(self, album):
        """
        View all albums with a name similar to the search argument with an ILIKE query assessing near-matches

        :param artist: Album name as a string
        :return: A list of lists  with album id, artist name, and album title the tracks from that album
                 NOT_FOUND if it cannot find any matches to the LIKE query
        """
        result = []
        with Session(self.database) as db:
           artist_id = db.execute("SELECT album_id, name, album_title FROM albums JOIN artists ON albums.artist_id = artists.artist_id WHERE album_title ILIKE :album_title_seg", {"album_title_seg": f"%{album}%"}).fetchall()

        if artist_id == []:
            return NOT_FOUND
        else:
            for artist in artist_id:
                result.append(artist)
        return result

    def view_track_lyrics(self, track, artist, album):
        """
        View a tracks lyrics

        :param track: Track name as a string
        :param artist: Artist name as a string
        :param album: Album name as a string
        :return: SUCCESS_NO_RESPONSE if a single track was found
                 NOT_FOUND in cases where it cannot find the track requested
                 MANY_FOUND if there is more than one response to the query
        :return: A list of track title, lyrics, artist name, and album title if a single track was found
                 A list of lists containing the track title, artist name, and album title of every query result if there is more than one response to the query 
                 None in the case where the check statement returns NOT_FOUND
        """
        result = []
        if artist == "!" and album == "!":
            with Session(self.database) as db:
                query = db.execute("SELECT track_title, lyrics, name, album_title FROM tracks JOIN albums ON tracks.album_id = albums.album_id JOIN artists ON albums.artist_id = artists.artist_id WHERE track_title ILIKE :track_title", {"track_title": track}).fetchall()
            if query == []:
                return NOT_FOUND, None
            elif len(query) > 1:
                for res in query:
                    result.append([res[0], res[2], res[3]])
                return MANY_FOUND, result
            else:
                return SUCCESS_NO_RESPONSE, [query[0]]

        elif artist != "!" and album != "!":
            with Session(self.database) as db:
                query = db.execute("SELECT track_title, lyrics, name, album_title FROM tracks JOIN albums ON tracks.album_id = albums.album_id JOIN artists ON albums.artist_id = artists.artist_id WHERE artists.name ILIKE :name AND albums.album_title ILIKE :album_title AND track_title ILIKE :track_title", {"name": artist, "album_title": album, "track_title": track}).fetchone()
            if query == None:
                return NOT_FOUND, None
            return SUCCESS_NO_RESPONSE, [query]
        else:
            return NOT_FOUND, None

    def lyric_lookup(self, searchparam):
        """
        View all tracks have lyrics containing the searchparam

        :param searchparam: Word or phrase to search for as a string
        :return: A list of lists for each track that has lyrics matching the string
                 NOT_FOUND if the matching finds no results
        """
        result = []
        with Session(self.database) as db:
            matches = db.execute("SELECT name, album_title, track_title FROM artists JOIN albums ON artists.artist_id = albums.artist_id JOIN tracks ON albums.album_id = tracks.album_id WHERE lyrics LIKE :lyrics", {"lyrics": "%"+searchparam+"%"}).fetchall()

        if matches != []:
            for match in matches:
                result.append(match)
        else:
            return NOT_FOUND
        return result

    def update_artist(self, artist, new_name):
        """
        Updates an artists name (via admin API) maintaining the artists id

        :param artist: Existing artists name as a string
        :param new_name: The new name that the artist should have as a string
        :return: SUCCESS_NO_RESPONSE if successful, or
                 NOT_FOUND if the existing artist cannot be found
        """
        with Session(self.database) as db:
            check = db.execute("SELECT artist_id FROM artists WHERE name ILIKE :artist", {"artist": artist}).fetchone()

        if check != None:
            with Session(self.database) as db:
                db.execute("UPDATE artists SET name = :new_name WHERE artist_id = :artist_id", {"new_name": new_name, "artist_id": check[0]})
                db.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NOT_FOUND

    def update_album(self, artist, album, new_title):
        """
        Updates an albums name (via admin API) maintaining the album id

        :param artist: The target artists name as a string
        :param album: The existing album title to be changed as a string
        :param new_name: The new title that the album should have as a string
        :return: SUCCESS_NO_RESPONSE if successful, or
                 NAME_COLLIDED if the intended new name is already in use, or
                 NOT_FOUND if the existing album cannot be found
        """
        with Session(self.database) as db:
            check = db.execute("SELECT albums.album_id, albums.artist_id FROM albums JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name ILIKE :artist AND albums.album_title ILIKE :album", {"artist": artist, "album": album}).fetchone()
        
        if check != None:
            with Session(self.database) as db:
                dupe_check = db.execute("SELECT albums.album_id, albums.artist_id FROM albums JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name ILIKE :artist AND albums.album_title ILIKE :album", {"artist": artist, "album": new_title}).fetchone()
            if dupe_check == None:
                with Session(self.database) as db:
                    db.execute("UPDATE albums SET album_title = :new_title WHERE album_id = :album_id AND artist_id = :artist_id", {"new_title": new_title, "album_id": check[0], "artist_id": check[1]})
                    db.commit()
                return SUCCESS_NO_RESPONSE
            return NAME_COLLIDED
        else:
            return NOT_FOUND

    def update_track(self, artist, album, track, new_title):
        """
        Updates a tracks title (via admin API) maintaining the track id

        :param artist: The target artists name as a string
        :param album: The target album title as a string
        :param track: The existing track title to be changed as a string
        :param new_name: The new title that the track should have as a string
        :return: SUCCESS_NO_RESPONSE if successful, or
                 NOT_FOUND if the existing track cannot be found
        """
        with Session(self.database) as db:
            check = db.execute("SELECT tracks.track_id, tracks.album_id FROM tracks JOIN albums ON tracks.album_ID = albums.album_id JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name ILIKE :artist AND albums.album_title ILIKE :album and tracks.track_title ILIKE :track", {"artist": artist, "album": album, "track": track}).fetchone()
        
        if check != None:
            with Session(self.database) as db:
                db.execute("UPDATE tracks SET track_title = :new_title WHERE track_id = :track_id AND album_id = :album_id", {"new_title": new_title, "track_id": check[0], "album_id": check[1]})
                db.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NOT_FOUND

    def update_lyrics(self, artist, album, track, new_lyrics):
        """
        Updates a tracks lyrics (via admin API) by directly overwriting them

        :param artist: The target artists name as a string
        :param album: The target album title as a string
        :param track: The target track title as a string
        :param new_lyrics: The new lyrics that the track should have as a string
        :return: SUCCESS_NO_RESPONSE if successful, or
                 NOT_FOUND if the existing track cannot be found
        """
        with Session(self.database) as db:
            check = db.execute("SELECT tracks.track_id, tracks.album_id FROM tracks JOIN albums ON tracks.album_ID = albums.album_id JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name ILIKE :artist AND albums.album_title ILIKE :album and tracks.track_title ILIKE :track", {"artist": artist, "album": album, "track": track}).fetchone()
        
        if check != None:
            with Session(self.database) as db:
                db.execute("UPDATE tracks SET lyrics = :new_lyrics WHERE track_id = :track_id AND album_id = :album_id", {"new_lyrics": new_lyrics, "track_id": check[0], "album_id": check[1]})
                db.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NOT_FOUND

    def delete_artist(self, artist):
        """
        Deletes an artist from the database (via admin API) with cascading deletes that remove all associated albums and tracks

        :param artist: The artist name to be deleted as a string
        :return: SUCCESS_NO_RESPONSE if successful, or
                 NOT_FOUND if the artist cannot be found
        """
        with Session(self.database) as db:
            check = db.execute("SELECT artist_id FROM artists WHERE name ILIKE :artist", {"artist": artist}).fetchone()

        if check != None:
            with Session(self.database) as db:
                db.execute("DELETE FROM artists WHERE artist_id = :artist_id", {"artist_id": check[0]})
                db.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NOT_FOUND

    def delete_album(self, artist, album):
        """
        Deletes an album from the database (via admin API) with cascading deletes that remove all associated tracks

        :param artist: The target artists name as a string
        :param album: The album to be deleted as a string
        :return: SUCCESS_NO_RESPONSE if successful, or
                 NOT_FOUND if the album cannot be found
        """
        with Session(self.database) as db:
            check = db.execute("SELECT albums.album_id FROM albums JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name ILIKE :artist AND albums.album_title ILIKE :album", {"artist": artist, "album": album}).fetchone()

        if check != None:
            with Session(self.database) as db:
                db.execute("DELETE FROM albums WHERE album_id = :album_id", {"album_id": check[0]})
                db.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NOT_FOUND

    def delete_track(self, artist, album, track):
        """
        Deletes a track from the database (via admin API)

        :param artist: The target artists name as a string
        :param album: The target album title as a string
        :param track: The track to be deleted as a string
        :return: SUCCESS_NO_RESPONSE if successful, or
                 NOT_FOUND if the album cannot be found
        """
        with Session(self.database) as db:
            check = db.execute("SELECT tracks.track_id, tracks.album_id FROM tracks JOIN albums ON tracks.album_ID = albums.album_id JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name ILIKE :artist AND albums.album_title ILIKE :album and tracks.track_title ILIKE :track", {"artist": artist, "album": album, "track": track}).fetchone()
        
        if check != None:
            with Session(self.database) as db:
                db.execute("DELETE FROM tracks WHERE track_id = :track_id AND album_id = :album_id", {"track_id": check[0], "album_id": check[1]})
                db.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NOT_FOUND

    def delete_lyrics(self, artist, album, track):
        """
        'Deletes' a tracks lyrics from the database (via admin API) by updating the lyrics with a Postgres NULL value

        :param artist: The target artists name as a string
        :param album: The target album title as a string
        :param track: The target track to have the lyrics removed from as a string
        :return: SUCCESS_NO_RESPONSE if successful, or
                 NOT_FOUND if the track cannot be found
        """
        with Session(self.database) as db:
            check = db.execute("SELECT tracks.track_id, tracks.album_id FROM tracks JOIN albums ON tracks.album_ID = albums.album_id JOIN artists ON artists.artist_id = albums.artist_id WHERE artists.name ILIKE :artist AND albums.album_title ILIKE :album and tracks.track_title ILIKE :track", {"artist": artist, "album": album, "track": track}).fetchone()
        
        if check != None:
            with Session(self.database) as db:
                db.execute("UPDATE tracks SET lyrics = NULL WHERE track_id = :track_id AND album_id = :album_id", {"track_id": check[0], "album_id": check[1]})
                db.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NOT_FOUND

    def close(self):
        """
        Close database access cleanly
        Used in unittesting to resolve multiple instantiations of the DbFunctions class
        """
        self.database.dispose()
