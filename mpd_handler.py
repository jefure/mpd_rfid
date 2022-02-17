from mpd import MPDClient, CommandError
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

HOST = config['DEFAULT']['MPD_HOST']
PORT = config['DEFAULT']['MPD_PORT']


def connect_mpd():
    """ Connect to the mpd server
    :return The mpd client
    """
    client = MPDClient()
    client.timeout = 10
    client.idletimeout = None
    client.connect(HOST, PORT)
    return client


def load_playlists(client):
    """
    Load all playlist from the mpd server
    :param client: The mpd client
    :return: The list of playlists
    """
    return client.listplaylists()


def load_playlist_info(client, playlist_name):
    """
    Load the information of the playlist with the provided name
    :param client: The mpd client
    :param playlist_name: The name of the playlist
    :return: The playlist information
    """
    return client.listplaylistinfo(playlist_name)


def play_playlist(client, playlist_name):
    """
    Load the playlist into the queue and start playing it
    :param client: The mpd client
    :param playlist_name: The name of the playlist
    :return: nothing
    """
    client.load(playlist_name)
    client.play(0)


def get_image(client, playlist):
    songs = load_playlist_info(client, playlist[1])
    try:
        song = songs[0]
        return load_image(client, song)
    except IndexError:
        print("Playlist has no songs: ", playlist)

    return {}


def load_image(client, song):
    image = {}
    try:
        image = client.readpicture(song["file"])
    except CommandError:
        print("No Image for ", song)

    return image
