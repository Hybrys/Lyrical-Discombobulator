from sqlite3 import connect

NOT_FOUND = 0
LESS_THAN_ZERO = 1
NAME_COLLIDED = 2
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
            "CREATE TABLE IF NOT EXISTS artists (artist_id INTEGER PRIMARY KEY, name TEXT, UNIQUE(name))")
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS albums (album_id INTEGER PRIMARY KEY, title TEXT, artist_id INTEGER, FOREIGN KEY(artist_id) REFERENCES artists(artist_id), UNIQUE(title, artist_id))")
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS tracks (track_id INTEGER PRIMARY KEY, title TEXT, track_num INTEGER, lyrics TEXT, album_id INTEGER, FOREIGN KEY(album_id) REFERENCES albums(album_id), UNIQUE(title, album_id))")

    def add_artist(self, artist, albums):
        """

        :param artist: Artist name as a string
        :param albums: Album names as a list
        """
        artist = artist.title()
        try:
            self.db.execute("INSERT INTO artists (name) VALUES (?)", (artist,))
            artist_id = self.db.lastrowid
        except:
            return NAME_COLLIDED
        if albums != None:
            for album in albums:
                self.db.execute(
                    "INSERT OR IGNORE INTO albums (title, artist_id) VALUES (?, ?)", (album, artist_id))
        self.database.commit()
        return SUCCESS_NO_RESPONSE

    def view_artistalbums(self, artist):
        """

        :param artist: Artist name as a string
        """
        result = self.db.execute(
            "SELECT item, count FROM inventory WHERE deleted = 0").fetchall()
        if result == []:
            return NOT_FOUND
        return result

    # for unittesting
    def close(self):
        self.database.close()
