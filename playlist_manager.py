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
import argparse

import mpd_handler as mpd
import repository as db


def main():
    args = get_args()
    conn = db.create_connection()
    client = mpd.connect_mpd()
    with conn:
        db.create_table(conn)
        db.store_playlists(mpd.load_playlists(client), conn)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--update',
                        action='store_true',
                        help="Update the playlist database")
    parser.add_argument('-t', '--test',
                        action='store_true',
                        help='Test the reading playlists from mpd server')
    parser.add_argument('-n', '--new',
                        action='store_true',
                        help='Drop the existing database and create a new one')
    return parser.parse_args()


if __name__ == '__main__':
    main()
