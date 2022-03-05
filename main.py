from itty3 import HTML, App, HttpResponse
from urllib.parse import unquote
import db

app = App()
database = db.DbFunctions()


@app.get("/")
def index(request):
    with open("index.html") as index_file:
        result = index_file.read()
    return app.render(request, result)


@app.get("/artist/<str:artist>")
def view_artist(request, artist):
    response = ["<table><tr><th>Artist</th><th>Album</th></tr>"]
    artist = unquote(artist)
    check = database.view_artist_albums(artist)
    if check != db.NOT_FOUND:
        for fetched_item in check:
            response.append(f"<tr><td>{fetched_item[0]}</td><td>{fetched_item[1]}</td></tr>")
        response = "".join(response) + "</table>"
        return HttpResponse(body=response, content_type=HTML)
    return HttpResponse(body="No items exist in the database yet!", content_type=HTML)


if __name__ == "__main__":
    app.run(port=4000, debug=True)
