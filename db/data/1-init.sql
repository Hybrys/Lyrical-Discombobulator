-- Reinitialize the database
DROP DATABASE IF EXISTS "database";
CREATE DATABASE "database";

DROP DATABASE IF EXISTS "test";
CREATE DATABASE "test";

CREATE INDEX albums_hash_index ON albums USING HASH (album_title);
CREATE INDEX tracks_hash_index ON tracks USING HASH (track_title);
