# Nathan C Spring 2022 Python Portfolio Project

## Purpose
This project consists of a webscraper to grab artists/albums/tracks/lyrics, as well as a frontend to access that data.

The database is pre-populated with over 1000 artists and 45000 tracks with lyrics, and the frontend allows you to search by:
 - Artist name
 - Album title
 - Track title
 - Word or phrase, searched against the lyrics

## Dependancies
Requires Python 3.8+ (Python 3.10.1 used)
Requires Docker v18 or higher (docker compose up -d)
 - Creates Postgres and pgAdmin containers for app usage

Requires Itty3 module for Python (pip install itty3)
Requires pg8000 module for Python (pip install pg8000)

## Usage
#### To run the server:
python3 main.py

#### To access the server:
Open a browser to http://localhost:4000

#### To run the scraper (currently only parsing lyrics):
python3 scraper.py

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
