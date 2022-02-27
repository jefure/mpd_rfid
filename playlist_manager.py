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
