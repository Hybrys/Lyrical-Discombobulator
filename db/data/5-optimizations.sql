\c database

-- In testing, these two hash indexes improved performance
-- Everything else is either unique or queried via PK
CREATE INDEX albums_hash_index ON albums(album_title);
CREATE INDEX tracks_hash_index ON tracks(track_title);

-- Fixes sequencing issues with the seeded database
SELECT setval(pg_get_serial_sequence('artists', 'artist_id'), coalesce(max(artist_id),0) + 1, false) FROM artists;
SELECT setval(pg_get_serial_sequence('albums', 'album_id'), coalesce(max(album_id),0) + 1, false) FROM albums;
SELECT setval(pg_get_serial_sequence('tracks', 'track_id'), coalesce(max(track_id),0) + 1, false) FROM tracks;
