from sqlite3 import IntegrityError
import re

"""
HERE BE DRAGONS

DANGEROUS - this is destructive
Created to allow running very specific commands to improve data quality
"""

import db

dbcur = db.DbFunctions()


for track in dbcur.view_unparsed_tracks():
    # paren_locator = track[2].lower().find("(live at")
    # paren_locator = re.search(r'live\sbootleg', track[2])
    if "instrumental" in track[2]:
        print(track[2])
        # try:
        #     dbcur.db.execute("UPDATE tracks SET track_title = (?) WHERE track_title = (?) AND album_id = (?)", (track[2][:paren_locator], track[2], track[3]))
        #     dbcur.commit()
        # except IntegrityError:
        #     pass
