# Portfolio Project API Documentation

## Purpose
This is to fulfill the API ask for the NuCamp Portfolio Project

This API is not intended to touch the main database store, and thus has an empty database 'test' initialized.

## Adding items to the database
#### Artist
    POST /addartist/:artist

    Adds the artist name of at least three characters in key ':artist' to the database.

    On success: HTTP Response ':artist added to the database!'
    On failure: HTTP Response 'Seems like most artists should contain more than two characters!'

#### Album
    POST /addalbum/:artist/:album

    Adds the album name at key ':album' of an existing artist at key ':artist' to the database.

    On success: HTTP Response 200 'Added :album for :artist to the album database!'
    On failure: 
                :artist doesn't exist in the database
                HTTP Response 500 'The artist :artist wasn't found in the database!  It needs to exist before we can add albums to it!'

                Too few characters in key :artist
                HTTP Response 500 'Seems like most artists should contain more than two characters!'

                Too few characters in key :album
                HTTP Response 500 'Seems like this album should contain more than two characters!'

#### Tracks
    POST /addtrack/:artist/:album/:track

    Adds the track name at key ':track' of an existing album at key :album and an existing artist at key ':artist' to the database.

    On success: HTTP Response 200 'Added :track from :album by :artist to the database!'
    On failure: 
                :album doesn't exist in the database
                HTTP Response 500 'The album :album wasn't found in the database!  It needs to exist before we can add tracks to it!'

                Too few characters in key :artist
                HTTP Response 500 'Seems like most artists should contain more than two characters!'

                Too few characters in key :album
                HTTP Response 500 'Seems like this album should contain more than two characters!'

#### Lyrics
    POST /addlyrics/:artist/:album/:track
    JSON body: {"lyrics": "example"}

    Adds the lyrics from JSON body key "lyrics" for existing track name at key ':track' of an existing album at key :album and an existing artist at key ':artist' to the database.

    On success: HTTP Response 200 'Added lyrics to the track :track!'
    On failure: 
                :track doesn't exist in the database
                HTTP Response 500 'The track :track wasn't found in the database!  It needs to exist before we can add lyrics to it!'

                JSON body key "lyrics" doesn't exist
                HTTP Response 500 'Seems like you should add some lyrics if you'd like to modify a track!  I'm checking against lyrics in the json data'

                JSON body key "lyrics" is empty
                HTTP Response 500 'We found 'lyrics' in the JSON, but you need to specify some actual lyrics!'

                Too few characters in key :artist
                HTTP Response 500 'Seems like most artists should contain more than two characters!'

                Too few characters in key :album
                HTTP Response 500 'Seems like this album should contain more than two characters!'

## Updating items in the database
#### Artist
    PUT /updateartist/:artist
    JSON body: {"artist": "new artist name"} or

    PATCH /updateartist/:artist
    JSON body: {"artist": "new artist name"}

    Updates the existing artist name from key :artist to the new JSON body key "artist"

    On success: HTTP Response 200 ':artist has been renamed to "artist"'
    On failure: 
                :artist doesn't exist in the database
                HTTP Response 500 'I can't find the original artist!'

                JSON body key "artist" doesn't exist
                HTTP Response 500 'You need to specify a new artist name in a JSON with the key 'artist'!'

                Too few characters in JSON body key "artist"
                HTTP Response 500 'The new artists name should also contain at least two characters!'

                Too few characters in key :artist
                HTTP Response 500 'Seems like most artists should contain at least two characters!'

#### Album
    PUT /updatealbum/:artist/:album
    JSON body: {"album": "new album name"} or

    PATCH /updatealbum/:artist/:album
    JSON body: {"album": "new album name"}

    Updates the existing album name from key :album to the new JSON body key "album"

    On success: HTTP Response 200 ':album has been renamed to "album"'
    On failure: 
                :album doesn't exist in the database
                HTTP Response 500 'I can't find the original album!'

                JSON body key "artist" doesn't exist
                HTTP Response 500 'You need to specify a new artist name in a JSON with the key 'album'!'

                Too few characters in JSON body key "artist"
                HTTP Response 500 'The new artists name should also contain at least two characters!'

                Too few characters in key :artist
                HTTP Response 500 'Seems like most artists should contain more than two characters!'

                Too few characters in key :album
                HTTP Response 500 'Seems like this album should contain more than two characters!'

#### Tracks
    PUT /updatetrack/:artist/:album/:track
    JSON body: {"track": "new track name"} or

    PATCH /updatetrack/:artist/:album/:track
    JSON body: {"track": "new track name"}

    Updates the existing track name from key :track to the new JSON body key "track"

    On success: HTTP Response 200 ':track has been renamed to "track"'
    On failure: 
                :track doesn't exist in the database
                HTTP Response 500 'I can't find the original track!'

                JSON body key "track" doesn't exist
                HTTP Response 500 'You need to specify a new artist name in a JSON with the key 'track'!'

                Too few characters in JSON body key "track"
                HTTP Response 500 'The new artists name should also contain at least one characters!'

                Too few characters in key :artist
                HTTP Response 500 'Seems like most artists should contain more than two characters!'

                Too few characters in key :album
                HTTP Response 500 'Seems like this album should contain more than two characters!'

#### Lyrics
    PUT /updatelyrics/:artist/:album/:track
    JSON body: {"lyrics": "new lyrics"} or

    PATCH /updatelyrics/:artist/:album/:track
    JSON body: {"lyrics": "new lyrics"}

    Updates the existing tracks lyrics from key :track to the new JSON body key "lyrics"

    On success: HTTP Response 200 ':track had its lyrics updated!'
    On failure: 
                :track doesn't exist in the database
                HTTP Response 500 'I can't find the original track!'

                JSON body key "track" doesn't exist
                HTTP Response 500 'Seems like you should add some lyrics if you'd like to modify a track!  I'm checking against 'lyrics' in the json data'

                Too few characters in key :artist
                HTTP Response 500 'Seems like most artists should contain more than two characters!'

                Too few characters in key :album
                HTTP Response 500 'Seems like this album should contain more than two characters!'

## Delete
#### Tracks
    DELETE /deletetrack/:artist/:album/:track

    Deletes the existing track name from key :track to the new JSON body key "track"

    On success: HTTP Response 200 ':track deleted!'
    On failure: 
                :track doesn't exist in the database
                HTTP Response 500 'I can't find that track!'

                Too few characters in key :artist
                HTTP Response 500 'Seems like most artists should contain more than two characters!'

                Too few characters in key :album
                HTTP Response 500 'Seems like this album should contain more than two characters!'