from sqlite3 import IntegrityError
import re

"""
HERE BE DRAGONS

DANGEROUS - this is destructive
Created to allow running very specific commands to improve data quality
"""

import db

dbcur = db.DbFunctions()

index = 0

for track in dbcur.second_pass_empty_tracks():
    if ")" == track[2][-1::]:
        if "instrumental" not in track[2] and "feat" not in track[2] and "remix" not in track[2] and "pt" not in track[2] and "part" not in track[2]:
            # if "originally" in track[2]:
            index += 1
            paren_locator = track[2].find("(", 1)
            print(track[2])
        # try:
            # dbcur.db.execute("UPDATE tracks SET track_title = (?) WHERE track_title = (?) AND album_id = (?)", (track[2][:paren_locator], track[2], track[3]))
            # dbcur.commit()
        # except IntegrityError:
        #     pass
print(index)
