# Nathan C Spring 2022 Python Portfolio Project

## Purpose
This project was created as a portfolio item, and was used as expanding education while attending NuCamp.  The intent was to create a simple artist/album/track/lyric search engine while experimenting with a variety of Python modules, test-driven development, pickles, and containerization.

This project uses BeautifulSoup as a webscraper to grab artists/albums/tracks/lyrics, SQLAlchemy and pg8000 to store the data in a Postgres server, as well as a JQuery frontend powered by Flask to access that data.  This project also uses NLTK and Syllapy to 'discombobulate' the lyrics, replacing each possible word based on similar syllabic structure and part-of-speech.

The database is pre-populated with over 1000 artists and 45000 tracks with lyrics. The frontend allows you to search by:
 - Artist name
 - Album title
 - Track title
 - Word or phrase, searched against the lyrics

 This project has 98% test coverage by line, with unit testing.  Integration and E2E testing to come.

## Dependancies
Requires Docker v18 or higher (docker compose up -d)
 - Creates Postgres and pgAdmin containers for app usage

## Usage
#### To run the server:
docker compose up -d

#### To access the server:
Open a browser to http://localhost:4000

#### To run the scraper manually:
Not yet implemented

## Indexing/Optimization
    All queries take less than 125ms to run.
    This was achieved with Hash Table indexing on album and track names

## Backups
    All data exists in SQL files for initial Docker startup
    These are dumped via the Windows program 'HeidiSQL' with some automation to update them on significant database changes

## TODO

#### Overall improvement / enhancement
- Implement the API from the nucamprequirements branch in a separate Docker container with authentication
- Expand on the API to include proper functionality to delete albums and artists (with cascades)
- Create a public-facing API that allows people to add new artists with validation
- Migrate the app to Django

#### Items for Scraper Improvement

 - Resolve accenting - websites simply drop the accents rather than accepting URI encoded characters
 - Resolve TypeErroring in parse_tracks - this should be raising AttributeErrors if the object doesn't exist, so some conditional type conversion may need to take place to resolve this
 - Create handler for parsing only artists that have no albums and albums that have no tracks - use LEFT JOIN on IDs where album_title and track_title IS NULL
 - Move from html.parser to LXML for ~25% speedup
 - Backtracking refactor (page by page stepping)
 - Consider edge-case handling by headless chrome instance (Playwright)


# API Documentation

## Purpose
This is an administrator-only API intended to allow for the easy and quick modification of database values

## Adding items to the database
#### Artist
    POST /addartist/:artist

    Adds the artist name of at least three characters in key ':artist' to the database.

    On success: HTTP Response ':artist added to the database!'
    On failure:                 
                Too few characters in key :artist
                HTTP Response 500 'Seems like most artists should contain more than two characters!'

                :artist already exists in the database
                HTTP Response 500 ':artist already exists in the database!'


#### Album
    POST /addalbum/:artist/:album

    Adds the album name at key ':album' of an existing artist at key ':artist' to the database.

    On success: HTTP Response 200 'Added :album for :artist to the database!'
    On failure: 
                Too few characters in :artist or :album
                HTTP Response 500 'Seems like most artists or albums should contain more than two characters!'

                :album referring to :artist already exists in the database
                HTTP Response 500 'The album :album by :artist already exists!'

                :artist doesn't exist in the database
                HTTP Response 500 'The artist :artist wasn't found in the database!'

#### Tracks
    POST /addtrack/:artist/:album/:track

    Adds the track name at key ':track' of an existing album at key :album and an existing artist at key ':artist' to the database.

    On success: HTTP Response 200 'Added :track from :album by :artist to the database!'
    On failure: 
                Too few characters in :artist or :album
                HTTP Response 500 'Seems like most artists or albums should contain more than two characters!'

                :track referring to :album and :artist already exists in the database
                HTTP Response 500 'The track ':track' on :album by :artist already exists!

                :album doesn't exist in the database
                HTTP Response 500 'The album :album wasn't found in the database!'

#### Lyrics
    POST /addlyrics/:artist/:album/:track
    JSON body: {'lyrics': "example"}

    Adds the lyrics from JSON body key 'lyrics' for existing track name at key ':track' of an existing album at key :album and an existing artist at key ':artist' to the database.

    On success: HTTP Response 200 'Added lyrics to the track :track!'
    On failure: 
                Too few characters in :artist or :album
                HTTP Response 500 'Seems like most artists or albums should contain more than two characters!'

                JSON body key 'lyrics' doesn't exist
                HTTP Response 500 'Seems like you should add some lyrics if you'd like to modify a track!  I'm checking against 'lyrics' in the JSON data'
                
                :track doesn't exist in the database
                HTTP Response 500 'The track :track wasn't found in the database!'

                JSON body key 'lyrics' is empty
                HTTP Response 500 'We found 'lyrics' in the JSON, but you need to specify some actual lyrics!'

## Updating items in the database
#### Artist
    PUT /updateartist/:artist
    JSON body: {'artist': 'new artist name'} or

    PATCH /updateartist/:artist
    JSON body: {'artist': 'new artist name'}

    Updates the existing artist name from key :artist to the new value in JSON body key 'artist'

    On success: HTTP Response 200 ':artist has been renamed to :(JSON body key 'artist' value)'
    On failure: 
                Too few characters in key :artist
                HTTP Response 500 'Seems like most artists should contain at least two characters!'

                JSON body key 'artist' doesn't exist
                HTTP Response 500 'You need to specify a new artist name in a JSON with the key 'artist'!'

                An integer exists in JSON body key 'artist'
                HTTP Response 500 'You need to wrap the name in quotes!  Integers won't work'

                Too few characters in JSON body key 'artist'
                HTTP Response 500 'The new artists name should also contain at least two characters!'

                :(JSON key 'artist' value) already exists in the database
                HTTP Response 500 'The artist :(JSON key 'artist' value) already exists!  Please pick another name to rename the artist to.'

                :artist doesn't exist in the database
                HTTP Response 500 'I can't find the original artist!'

#### Album
    PUT /updatealbum/:artist/:album
    JSON body: {'album': 'new album name'} or

    PATCH /updatealbum/:artist/:album
    JSON body: {'album': 'new album name'}

    Updates the existing album name from key :album to the new value in JSON body key 'album'

    On success: HTTP Response 200 ':album has been renamed to :(JSON body key 'album' value)'
    On failure: 
                Too few characters in :artist or :album
                HTTP Response 500 'Seems like most artists or albums should contain more than two characters!'

                JSON body key 'album' doesn't exist
                HTTP Response 500 'You need to specify a new artist name in a JSON with the key 'album'!'

                An integer exists in JSON body key 'album'
                HTTP Response 500 'You need to wrap the name in quotes!  Integers won't work'

                Too few characters in JSON body key 'album'
                HTTP Response 500 'The new albums name should also contain at least two characters!'

                :(JSON body key 'album' value) referring to :artist already exists in the database
                HTTP Response 500 'The album :(JSON body key 'album' value) by :artist already exists!'

                :album doesn't exist in the database
                HTTP Response 500 'I can't find the original album!'

#### Tracks
    PUT /updatetrack/:artist/:album/:track
    JSON body: {'track': 'new track name'} or

    PATCH /updatetrack/:artist/:album/:track
    JSON body: {'track': 'new track name'}

    Updates the existing track name from key :track to the new value in JSON body key 'track'

    On success: HTTP Response 200 ':track has been renamed to :(JSON body key 'track' value)'
    On failure: 
                Too few characters in :artist or :album
                HTTP Response 500 'Seems like most artists or albums should contain more than two characters!'

                JSON body key 'track' doesn't exist
                HTTP Response 500 'You need to specify a new artist name in a JSON with the key 'track'!'

                An integer exists in JSON body key 'track'
                HTTP Response 500 'You need to wrap the name in quotes!  Integers won't work'

                Too few characters in JSON body key 'track'
                HTTP Response 500 'The new artists name should also contain at least one characters!'

                :(JSON body key 'track' value) referring to :album and :artist already exists in the database
                HTTP Response 500 'The track ':(JSON body key 'track' value)' on :album by :artist already exists!'

                :track doesn't exist in the database
                HTTP Response 500 'I can't find the original track!'


#### Lyrics
    PUT /updatelyrics/:artist/:album/:track
    JSON body: {'lyrics': 'new lyrics'} or

    PATCH /updatelyrics/:artist/:album/:track
    JSON body: {'lyrics': 'new lyrics'}

    Updates the existing tracks lyrics from key :track to the new value in JSON body key 'lyrics'

    On success: HTTP Response 200 ':track had its lyrics updated!'
    On failure: 
                Too few characters in :artist or :album
                HTTP Response 500 'Seems like most artists or albums should contain more than two characters!'

                JSON body key 'lyrics' doesn't exist
                HTTP Response 500 'Seems like you should add some lyrics if you'd like to modify a track!  I'm checking against 'lyrics' in the json data'

                :track doesn't exist in the database
                HTTP Response 500 'I can't find the original track!'



## Delete
#### Artists
    DELETE /deleteartist/:artist
    JSON body: {'confirm': 'True'}

    Deletes the existing artist from key :artist from the database
    Cascades removing all referenced albums and tracks

    On success: HTTP Response 200 ':artist has been deleted!'
    On failure: 
                Too few characters in key :artist
                HTTP Response 500 'Seems like most artists should contain more than two characters!'

                JSON body key 'confirm' doesn't exist
                HTTP Response 500 'If you'd really like to delete an artist and its albums/tracks, please include 'confirm': 'True' in the JSON body.\n\nWarning, this will delete all associated albums/tracks.'

                JSON body key 'confirm' does not have the value 'True'
                HTTP Response 500 'You'll need to take the safety off - please include 'confirm': 'True' in the JSON body.\n\nWarning, this will delete all associated albums/tracks.'

                :track doesn't exist in the database
                HTTP Response 500 'I can't find the artist :artist!'

#### Albums
    DELETE /deletealbum/:artist/:album
    JSON body: {'confirm': 'True'}

    Deletes the existing album from key :album referring to key :artist from the database
    Cascades removing all referenced tracks

    On success: HTTP Response 200 ':album has been deleted!'
    On failure: 
                Too few characters in :artist or :album
                HTTP Response 500 'Seems like most artists or albums should contain more than two characters!'

                JSON body key 'confirm' doesn't exist
                HTTP Response 500 'If you'd really like to delete an artist and its albums/tracks, please include 'confirm': 'True' in the JSON body.\n\nWarning, this will delete all associated albums/tracks.'

                JSON body key 'confirm' does not have the value 'True'
                HTTP Response 500 'You'll need to take the safety off - please include 'confirm': 'True' in the JSON body.\n\nWarning, this will delete all associated albums/tracks.'

                :album related to :artist doesn't exist in the database
                HTTP Response 500 'I can't find the album :album by :artist!'

#### Tracks
    DELETE /deletetrack/:artist/:album/:track
    JSON body: {'confirm': 'True'}

    Deletes the existing track name from key :track referring to keys :artist and :album from the database

    On success: HTTP Response 200 ':track has been deleted!'
    On failure: 
                Too few characters in :artist or :album
                HTTP Response 500 'Seems like most artists or albums should contain more than two characters!'

                JSON body key 'confirm' doesn't exist
                HTTP Response 500 'If you'd really like to delete an artist and its albums/tracks, please include 'confirm': 'True' in the JSON body.\n\nWarning, this will delete all associated albums/tracks.'

                JSON body key 'confirm' does not have the value 'True'
                HTTP Response 500 'You'll need to take the safety off - please include 'confirm': 'True' in the JSON body.\n\nWarning, this will delete all associated albums/tracks.'

                :track doesn't exist in the database
                HTTP Response 500 'I can't find :track from the album :album by :artist!'

### Lyrics
    DELETE /deletelyrics/:artist/:album/:track
    JSON body: {'confirm': 'True'}

    Deletes the existing lyrics from the track in key :track referring to keys :artist and :album from the database

    On success: HTTP Response 200 ':track had its lyrics emptied!'
    On failure: 
                Too few characters in :artist or :album
                HTTP Response 500 'Seems like most artists or albums should contain more than two characters!'

                JSON body key 'confirm' doesn't exist
                HTTP Response 500 'If you'd really like to delete an artist and its albums/tracks, please include 'confirm': 'True' in the JSON body.\n\nWarning, this will delete all associated albums/tracks.'

                JSON body key 'confirm' does not have the value 'True'
                HTTP Response 500 'You'll need to take the safety off - please include 'confirm': 'True' in the JSON body.\n\nWarning, this will delete all associated albums/tracks.'

                :track doesn't exist in the database
                HTTP Response 500 'I can't find :track from the album :album by :artist!'