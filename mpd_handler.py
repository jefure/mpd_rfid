from mpd import MPDClient
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def connect_mpd(host, port):
    """ Connect to the mpd server
    :param host: The host uri
    :param port: The port
    :return The mpd client
    """
    client = MPDClient()
    client.timeout = 10
    client.idletimeout = None
    client.connect(config['DEFAULT']['MPD_HOST'], config['DEFAULT']['MPD_PORT'])
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
