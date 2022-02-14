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
    mpd_client = mpd.connect_mpd("aki.fritz.box", 6600)
    print(playlist_name)
    print(mpd.load_playlist_info(mpd_client, playlist_name))
    mpd.play_playlist(mpd_client, playlist_name)
    return redirect(url_for('index'))

