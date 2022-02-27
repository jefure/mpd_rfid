#!/usr/bin/env python

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
        rfid = reader.read_rfid()
        exit()

    query = args.playlist
    print("Query:", query)
    playlists = db.get_all_playlists()
    for playlist in playlists:
        if query is None:
            process_with_skip(args, playlist)
        else:
            if bool(re.match(query, playlist[1], re.I)):
                process_with_skip(args, playlist)


def process_with_skip(args, playlist):
    if args.skip_with_rfid:
        if playlist[2] != -1:
            process_playlist(playlist[1])
    else:
        process_playlist(playlist[1])


def process_playlist(playlist_name):
    user_choice = get_user_input(playlist_name)
    if user_choice == 'a':
        rfid = reader.read_rfid()
        db.set_rfid_to_playlist(rfid, playlist_name)
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
