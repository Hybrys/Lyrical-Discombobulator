from sqlite3 import connect

NOT_FOUND = 0
NAME_COLLIDED = 1
NO_ITEM_TO_ADD = 2
SUCCESS_NO_RESPONSE = 3


class DbFunctions():
    def __init__(self, filename="database.db"):
        """
        Initialize the database for use - create the tables and file if it doesn't exist.

        :param filename: Optional param for using a test database
        """
        self.database = connect(filename)
        self.db = self.database.cursor()
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS artists (artist_id INTEGER PRIMARY KEY, name TEXT, isparsed INTEGER, UNIQUE(name))")
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS albums (album_id INTEGER PRIMARY KEY, album_title TEXT, artist_id INTEGER, isparsed INTEGER, FOREIGN KEY(artist_id) REFERENCES artists(artist_id), UNIQUE(album_title, artist_id))")
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS tracks (track_id INTEGER PRIMARY KEY, track_title TEXT, track_num INTEGER, lyrics TEXT, album_id INTEGER, parse_tried INTEGER, FOREIGN KEY(album_id) REFERENCES albums(album_id), UNIQUE(track_title, album_id))")

    def add_artist(self, artist):
        """
        Adds one single artist to the database

        :param artist: The name of the artist to add
        """
        name_test = self.db.execute("SELECT * FROM artists WHERE name = (?)", (artist,)).fetchone()
        if name_test == None:
            self.db.execute("INSERT INTO artists (name, isparsed) VALUES (?, ?)", (artist, 0))
            self.database.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NAME_COLLIDED

    def add_artist_albums(self, artist, albums):
        """
        Adds the artist to the artists database, and their albums to the albums database with a reference to which artist it belongs

        :param artist: Artist name as a string
        :param albums: Album names as a list
        :return: Returns SUCCESS_NO_RESPONSE if successful or NO_ITEM_TO_ADD if the list of albums is empty
        """

        if albums != None:
            artist_id = self.db.execute("SELECT artist_id FROM artists WHERE name = (?)", (artist[0],)).fetchone()[0]
            for album in albums:
                self.db.execute("INSERT OR IGNORE INTO albums (album_title, artist_id, isparsed) VALUES (?, ?, ?)", (album, artist_id, 0))
            self.db.execute("UPDATE artists SET isparsed = (?) WHERE name = (?)", (1, artist[0]))
            self.database.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NO_ITEM_TO_ADD

    def add_album_tracks(self, artist, album, tracks):
        """
        Add tracks to the 'tracks' database, referencing the album name

        :param artist: The artist name as a string
        :param album: The album name as a string
        :param tracks: The tracks as a list
        :return: Returns SUCCESS_NO_RESPONSE if successful, NOT_FOUND if it cannot find a match between artist and album, and NO_ITEM_TO_ADD if the list of tracks is empty
        """
        if tracks != [] and tracks != None:
            album_id = self.album_artist_match(artist, album)
            if album_id == NOT_FOUND:
                return NOT_FOUND
            for index, track in enumerate(tracks):
                self.db.execute("INSERT OR IGNORE INTO tracks (track_title, track_num, album_id) VALUES (?, ?, ?)", (track, index+1, album_id))
            self.db.execute("UPDATE albums SET isparsed = (?) WHERE album_title = (?)", (1, album))
            self.database.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NO_ITEM_TO_ADD

    def add_track_lyrics(self, artist, album, track, lyrics):
        """
        Add lyrics to the 'tracks' database, referencing the track name

        :param artist: The artist name as a string
        :param album: The album name as a string
        :param track: The track name as a string
        :return: Returns SUCCESS_NO_RESPONSE if successful, NOT_FOUND if it cannot find a match between artist and album, or track name and album id, and NO_ITEM_TO_ADD if the track string is empty
        """
        album_id = self.album_artist_match(artist, album)
        track_check = self.db.execute("SELECT track_title FROM tracks WHERE track_title = (?) AND album_id = (?)", (track, album_id)).fetchone()
        if album_id == NOT_FOUND:
            return NOT_FOUND

        if lyrics != "" and lyrics != None:
            if track_check != None:
                self.db.execute("UPDATE tracks SET lyrics = (?), parse_tried = (?) WHERE track_title = (?) AND album_id = (?)", (lyrics, 1, track, album_id))
                self.database.commit()
                return SUCCESS_NO_RESPONSE
            else:
                return NOT_FOUND
        else:
            self.db.execute("UPDATE tracks SET parse_tried = (?) WHERE track_title = (?) AND album_id = (?)", (1, track, album_id))
            self.database.commit()
            return NO_ITEM_TO_ADD

    def album_artist_match(self, artist, album):
        """
        Artist to album matching for cases in which the album title matches against more than one album

        :param artist: The name of the artist to match the ID of
        :param album: The name of the album to match the name of
        :returns: The artist ID of the first match between album name and artist name.
        """
        album_name_match = self.db.execute("SELECT artist_id, album_id FROM albums WHERE album_title = (?)", (album,)).fetchall()
        for matches in album_name_match:
            artist_check = self.db.execute("SELECT name FROM artists WHERE artist_id = (?)", (matches[0],)).fetchone()
            if artist_check[0] == artist:
                return matches[1]
            else:
                continue
        return NOT_FOUND

    def view_unparsed_artists(self):
        """
        View all artists that are not yet parsed

        :return: Returns a list of the artists that have a False for the isparsed flag
        """
        result = []
        artists = self.db.execute("SELECT name FROM artists WHERE isparsed = (?)", (0,)).fetchall()
        for artist in artists:
            result.append(artist[0])
        return result

    def view_unparsed_albums(self):
        """
        View all artists that are not yet parsed

        :return: Returns a list of lists for each artist that have a False for the isparsed flag, with each list containing the album and artist name
        """
        result = []
        unparsed_albums = self.db.execute("SELECT album_title, artist_id FROM albums WHERE isparsed = (?)", (0,)).fetchall()
        for album in unparsed_albums:
            artist_name = self.db.execute("SELECT name FROM artists WHERE artist_id = (?)", (album[1],)).fetchone()
            result.append([artist_name[0], album[0]])
        return result

    # Checks for first pass missed tracks
    # New variable 'parse_tried' in the tracks table will let us check second pass tracks
    def view_unparsed_tracks(self):
        """
        View all tracks that have an empty lyrics field and an empty parse_tried flag

        :return: Returns a list of lists where each list contains the artist name, album title, and track title
        """
        result = []
        unparsed_tracks = self.db.execute("SELECT track_title, album_id FROM tracks WHERE lyrics IS (?) AND parse_tried IS (?)", (None, None)).fetchall()
        for track in unparsed_tracks:
            album_info = self.db.execute("SELECT album_title, artist_id FROM albums WHERE album_id = (?)", (track[1],)).fetchone()
            artist_name = self.db.execute("SELECT name FROM artists WHERE artist_id = (?)", (album_info[1],)).fetchone()
            result.append([artist_name[0], album_info[0], track[0]])
        return result

    # Checks for first pass missed tracks
    def second_pass_empty_tracks(self):
        """
        View all tracks that still contain no lyrics after the first pass, where the lyrics field remains empty but 'parse_tried' = True

        :return: Returns a list of lists for each artist that have a False for the isparsed flag, with each list containing the track and artist name
        """
        result = []
        unparsed_tracks = self.db.execute("SELECT track_title, album_id FROM tracks WHERE lyrics IS (?) AND parse_tried = (?)", (None, 1)).fetchall()
        for track in unparsed_tracks:
            album_info = self.db.execute("SELECT album_title, artist_id FROM albums WHERE album_id = (?)", (track[1],)).fetchone()
            artist_name = self.db.execute("SELECT name FROM artists WHERE artist_id = (?)", (album_info[1],)).fetchone()
            result.append([artist_name[0], album_info[0], track[0]])
        return result

    def view_artist_albums(self, artist):
        """
        View all of an artists albums

        :param artist: Artist name as a string
        :return: Returns a list of the artists albums, or NOT_FOUND if there are none.
        """
        artist_id = self.db.execute("SELECT artist_id FROM artists WHERE name = (?)", (artist,))
        result = self.db.execute("SELECT title FROM albums WHERE artist_id = (?)", (artist_id,)).fetchall()
        if result == []:
            return NOT_FOUND
        return result

    def view_album_tracks(self, album):
        """
        View all of an albums tracks

        :param artist: Album name as a string
        :return: Returns a list of the tracks from that album, or NOT_FOUND if there are none.
        """
        album_id = self.db.execute("SELECT album_id FROM albums WHERE name = (?)", (album,))
        result = self.db.execute("SELECT track_title FROM tracks WHERE album_id = (?)", (album_id,)).fetchall()
        if result == []:
            return NOT_FOUND
        return result

    # for future unittesting
    def close(self):
        self.database.close()

    def commit(self):
        self.database.commit()
