#!/usr/bin/env python

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

from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
import repository as db
import rc522_reader as reader
import argparse
import re


menu_style = Style.from_dict({
    'dialog': 'bg:#88ff88',
    'dialog frame.label': 'bg:#ffffff #000000',
    'dialog.body': 'bg:#000000 #00ff00',
    'dialog shadow': 'bg:#00aa00',
})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--skip_with_rfid',
                        action='store_true',
                        help="Do not ask for RFID when the entry has already a RFID")
    parser.add_argument('-t', '--test_reader',
                        action='store_true',
                        help='Test the rfid reader')
    parser.add_argument('-p', '--playlist', help='Process playlists starting with the entered characters')
    args = parser.parse_args()
    if args.test_reader:
        reader.read_rfid()
        exit()

    query = args.playlist

    if query is None:
        playlists = db.get_all_playlists()
    else:
        playlists = db.search_playlist(query)

    for playlist in playlists:
        process_with_skip(args, playlist)


def process_with_skip(args, playlist):
    if args.skip_with_rfid:
        if playlist[2] != -1:
            process_playlist(playlist)
    else:
        process_playlist(playlist)


def process_playlist(playlist):
    user_choice = get_user_input(playlist[1])
    if user_choice == 'a':
        rfid = reader.read_rfid()
        db.set_rfid_to_playlist(rfid, playlist[0])
    elif user_choice == 'x':
        reader.cleanup()
        exit()


def get_user_input(playlist_name):
    result = button_dialog(
        title='Add RFID to playlist',
        text=HTML('<style fg="ansiwhite">Do you want to add a RFID to the playlist</style>\n'
                  '<i>{}</i>\n').format(playlist_name),
        buttons=[
            ('Yes', 'a'),
            ('No', 's'),
            ('Exit', 'x')
        ],
        style=menu_style
    ).run()
    return result


if __name__ == '__main__':
    main()
