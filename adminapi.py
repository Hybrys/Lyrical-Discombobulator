"""
This API is intended to fill the requirements for the Portfolio Project for NuCamp Spring 2022

THIS API IS NOT INTENDED TO GO LIVE AND SHOULD NOT BE DEPLOYED AS IT IS POTENTIALLY AND INTENTIONALLY DESTRUCTIVE
"""

from flask import Blueprint, Response
import db.db_postgres as db

database = db.DbFunctions()

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('', methods=['GET'])
def index():
    Response("This route serves a potential index page - a starting point.  It's not intended to be accessed, as I am merely a teapot.  Please read the documentation in api.md", status=418)

@bp.route('/addartist/<string:object>', methods=['POST'])
def add_artist(object):
    resp = database.add_artists([object])
    if resp == 87
    print(f"Adding {object.title()} to the artist database!")

@bp.route('/addartist/<string:object>', methods=['POST'])
def add(object):
