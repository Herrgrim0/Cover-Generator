from flask import render_template
from app import app
from .random_band_generator import AlbumGenerator


@app.route('/')
@app.route('/index')
def index():
    Album = AlbumGenerator()
    Album.create_album()
    page_title = str(Album)
    page_image = "/static/" + Album.get_album_url()

    data = {'title': page_title, 'cover': page_image}

    return render_template('index.html', data=data)
