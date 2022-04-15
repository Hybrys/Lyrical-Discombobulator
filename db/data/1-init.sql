-- Reinitialize the database
DROP DATABASE IF EXISTS "database";
CREATE DATABASE "database";

DROP DATABASE IF EXISTS "test";
CREATE DATABASE "test";

-- In testing, these two hash indexes improved performance
-- Everything else is either unique or queried via PK
CREATE INDEX albums_hash_index ON albums(album_title);
CREATE INDEX tracks_hash_index ON tracks(track_title);