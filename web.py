from flask import Flask, render_template, flash, url_for
from werkzeug.utils import redirect

import repository as db
import mpd_handler as mpd

app = Flask(__name__)


@app.route("/")
def index():
    playlists = db.get_all_playlists()
    return render_template('playlists.html', playlists=playlists)


@app.route('/<int:playlist_id>/play', methods=('POST',))
def play(playlist_id):
    playlist_name = db.get_playlist(playlist_id)
    mpd_client = mpd.connect_mpd()
    print(playlist_name)
    print(mpd.load_playlist_info(mpd_client, playlist_name))
    mpd.play_playlist(mpd_client, playlist_name)
    return redirect(url_for('index'))


@app.route("/covers")
def covers():
    db_playlists = db.get_all_playlists()
    display_playlists = []
    mpd_client = mpd.connect_mpd()
    for playlist in db_playlists:
        entry = [playlist[0], playlist[1], playlist[2]]
        image = mpd.get_image(mpd_client, playlist)
        entry.append(image)
        display_playlists.append(entry)

    return render_template('coverview.html', playlists=display_playlists)

