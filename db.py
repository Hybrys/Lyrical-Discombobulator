from sqlite3 import connect

NOT_FOUND = 0
NAME_COLLIDED = 1
NO_ITEM_IN_LIST = 2
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
            "CREATE TABLE IF NOT EXISTS tracks (track_id INTEGER PRIMARY KEY, title TEXT, track_num INTEGER, lyrics TEXT, album_id INTEGER, FOREIGN KEY(album_id) REFERENCES albums(album_id), UNIQUE(title, album_id))")

    def add_artist_albums(self, artist, albums):
        """
        Adds the artist to the artists database, and their albums to the albums database with a reference to which artist it belongs

        :param artist: Artist name as a string
        :param albums: Album names as a list
        """
        try:
            self.db.execute("INSERT INTO artists (name) VALUES (?)", (artist,))
            artist_id = self.db.lastrowid
        except:
            return NAME_COLLIDED

        if albums != None:
            for album in albums:
                self.db.execute(
                    "INSERT OR IGNORE INTO albums (album_title, artist_id) VALUES (?, ?)", (album, artist_id))
            self.db.execute("UPDATE artists SET isparsed = (?) WHERE name = (?)", (1, artist))
        else:
            return NO_ITEM_IN_LIST
        self.database.commit()
        return SUCCESS_NO_RESPONSE

    def add_album_tracks(self, artist, album, tracks):
        """
        Add tracks to the 'tracks' database, referencing the album name

        :param artist: The artist name as a string
        :param album: The album name as a string
        :param tracks: The tracks as a list
        :return: Returns SUCCESS_NO_RESPONSE if successful, NOT_FOUND if it cannot find a match between artist and album, and NONE if the list of tracks is empty
        """
        album_id = self.album_artist_match(artist, album)
        if album_id == NOT_FOUND:
            return NOT_FOUND
        print(album_id)
        if tracks != []:
            for index, track in enumerate(tracks):
                self.db.execute("INSERT OR IGNORE INTO tracks (title, track_num, album_id) VALUES (?, ?, ?)", (track, index+1, album_id))
            self.db.execute("UPDATE albums SET isparsed = (?) WHERE album_title = (?)", (1, album))
            self.database.commit()
            return SUCCESS_NO_RESPONSE
        else:
            return NO_ITEM_IN_LIST

    def album_artist_match(self, artist, album):
        """
        Artist to album matching for cases in which the album title matches against more than one album

        :param artist: The name of the artist to match the ID of
        :param album: The name of the album to match the name of
        :returns: The artist ID of the first match between album name and artist name.
        """
        album_name_match = self.db.execute(
            "SELECT album_title, artist_id, album_id FROM albums WHERE album_title = (?)", (album,)).fetchall()
        for matches in album_name_match:
            artist_check = self.db.execute(
                "SELECT name FROM artists WHERE artist_id = (?)", (matches[1],)).fetchone()
            if artist_check[0] == artist:
                return matches[2]
            else:
                return NOT_FOUND

    def view_artist_albums(self, artist):
        """
        View all of an artists albums

        :param artist: Artist name as a string
        :return: Returns a list of the artists albums, or NOT_FOUND if there are none.
        """
        artist_id = self.db.execute(
            "SELECT artist_id FROM artists WHERE name = (?)", (artist,))
        result = self.db.execute(
            "SELECT title FROM albums WHERE artist_id = (?)", (artist_id,)).fetchall()
        if result == []:
            return NOT_FOUND
        return result

    def view_album_tracks(self, album):
        """
        View all of an albums tracks

        :param artist: Album name as a string
        :return: Returns a list of the tracks from that album, or NOT_FOUND if there are none.
        """
        album_id = self.db.execute(
            "SELECT album_id FROM albums WHERE name = (?)", (album,))
        result = self.db.execute(
            "SELECT title FROM tracks WHERE album_id = (?)", (album_id,)).fetchall()
        if result == []:
            return NOT_FOUND
        return result

    # for unittesting
    def close(self):
        self.database.close()
