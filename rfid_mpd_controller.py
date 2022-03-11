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
        if playlist_name is not current_playlist:
            play_playlist(playlist_name)
            current_playlist = playlist_name


def play_playlist(playlist_name):
    print("Playing:", playlist_name)
    client = mpd.connect_mpd()
    mpd.clear_current_playlist(client)
    mpd.play_playlist(client, playlist_name)


if __name__ == '__main__':
    main()
