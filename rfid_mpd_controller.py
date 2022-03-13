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
import repository as db
import mpd_handler as mpd
import rc522_reader as reader

current_playlist = ""


def main():
    read_rfid()


def read_rfid():
    global current_playlist
    while True:
        rfid = reader.read_rfid()
        playlist_name = db.get_playlist_by_rfid(rfid)
        if playlist_name != current_playlist:
            play_playlist(playlist_name)
            current_playlist = playlist_name


def play_playlist(playlist_name):
    print("Playing:", playlist_name)
    client = mpd.connect_mpd()
    mpd.clear_current_playlist(client)
    mpd.play_playlist(client, playlist_name)


if __name__ == '__main__':
    main()
