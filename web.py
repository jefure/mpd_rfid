#
# This file is part of the mpd_rfid distribution (https://github.com/jefure/mpd_rfid).
# Copyright (c) 2022 Jens Reese.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import base64

from flask import Flask, render_template, url_for
from mpd import CommandError
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
    mpd.play_playlist(mpd_client, playlist_name)
    return redirect(url_for('index'))


@app.route("/covers")
def covers():
    db_playlists = db.get_all_playlists()
    display_playlists = []
    mpd_client = mpd.connect_mpd()
    for playlist in db_playlists:
        entry = [playlist[0], playlist[1], playlist[2]]
        try:
            dataurl = image_to_data_url(mpd.get_image(mpd_client, playlist))
            entry.append(dataurl)
            display_playlists.append(entry)
        except CommandError:
            print("Command error happened")

    return render_template('coverview.html', playlists=display_playlists)


def image_to_data_url(image):
    if image.get('type') is None:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    else:
        encoded_image = base64.b64encode(image.get('binary')).decode("utf-8")
        return "data:" + str(image.get('type')) + ";base64," + encoded_image
