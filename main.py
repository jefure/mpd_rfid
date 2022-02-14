# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import mpd_handler as mpd
import repository as db


def init():
    conn = db.create_connection()
    client = mpd.connect_mpd()
    with conn:
        db.create_table(conn)
        db.store_playlists(mpd.load_playlists(client), conn)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init()
