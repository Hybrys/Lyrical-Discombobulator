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

## TODO
#### Items for Future Improvement

 - Resolve accenting - websites simply drop the accents rather than accepting URI encoded characters
 - Resolve TypeErroring in parse_tracks - this should be raising AttributeErrors if the object doesn't exist, so some conditional type conversion may need to take place to resolve this
 - Implement unittesting
 - Allow user-curated input
 - Create handler for parsing only artists that have no albums and albums that have no tracks - use LEFT JOIN on IDs where album_title and track_title IS NULL
 - Move from html.parser to LXML for ~25% speedup
 - Backtracking refactor (page by page stepping)
 - Consider edge-case handling by headless chrome instance (Playwright)
