import sqlite3
from sqlite3 import Error
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

DB_FILE = config['DEFAULT']['DB_FILE']

CREATE_PLAYLIST_TABLE = '''
CREATE TABLE IF NOT EXISTS playlistKeys (
   id integer PRIMARY KEY,
   playlist_name NOT NULL,
   rfid text,
   added_date text
);
'''

INSERT_PLAYLIST = '''
INSERT INTO playlistKeys(playlist_name,rfid,added_date) VALUES (?,?,?)
'''

LIST_PLAYLISTS = '''
SELECT id,playlist_name,rfid,added_date FROM playlistKeys ORDER BY playlist_name
'''

SELECT_PLAYLIST = '''
SELECT playlist_name FROM playlistKeys WHERE id = ?
'''

SELECT_PLAYLIST_BY_RFID = '''
SELECT playlist_name FROM playlistKeys WHERE rfid = ?
'''

SET_RFID = '''
UPDATE playlistKeys SET rfid = ? WHERE id = ?
'''


def create_connection():
    """
    Create a database connection to a SQLite database
    :return The database connection
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
    except Error as e:
        print(e)
        if conn:
            conn.close()

    return conn


def create_table(conn):
    """
    Create a table from the create_table_sql statement
    :param conn: Connection object
    """
    try:
        c = conn.cursor()
        c.execute(CREATE_PLAYLIST_TABLE)
    except Error as e:
        print(e)


def store_playlists(playlists, conn):
    """
    Store all playlists in the database
    :param playlists: The List of playlists
    :param conn: The database connection
    """
    for playlist in playlists:
        playlist["rfid"] = "-1"
        print(playlist)
        add_playlist(conn, playlist)


def add_playlist(conn, playlist):
    """
    Create a new project into the projects table
    :param conn: The database connection
    :param playlist
    :return: playlist id
    """
    cur = conn.cursor()
    cur.execute(INSERT_PLAYLIST, (playlist['playlist'], playlist['rfid'], playlist['last-modified']))
    conn.commit()
    return cur.lastrowid


def get_all_playlists():
    """
    Load all playlists from the database
    :return: The playlists
    """
    conn = create_connection()
    playlists = conn.execute(LIST_PLAYLISTS).fetchall()
    conn.close()
    return playlists


def get_playlist(playlist_id):
    """
    Get the playlist identified by the id
    :param playlist_id: The database id of the playlist
    :return: The playlist name
    """
    conn = create_connection()
    playlist = conn.execute(SELECT_PLAYLIST, (playlist_id,)).fetchone()[0]
    conn.close()
    return playlist


def get_playlist_by_rfid(rfid):
    """
    Get the playlist identified by the rfid
    :param rfid: The stored rfid of the playlist
    :return: The playlist name
    """
    conn = create_connection()
    playlist = conn.execute(SELECT_PLAYLIST_BY_RFID, (rfid,)).fetchone()[0]
    conn.close()
    return playlist


def set_rfid_to_playlist(rfid, playlist_id):
    """
    Add or update the rfid value of a playlist entry
    :param rfid: The rfid value to set
    :param playlist_id: The database id of the playlist
    """
    conn = create_connection()
    conn.execute(SET_RFID, (rfid, playlist_id,))
    conn.close()
