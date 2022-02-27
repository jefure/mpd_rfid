import repository as db
import mpd_handler as mpd
import rc522_reader as reader


def main():
    rfid = reader.read_rfid()
    playlist_name = db.get_playlist_by_rfid(rfid)
    client = mpd.connect_mpd()
    mpd.play_playlist(client, playlist_name)


if __name__ == '__main__':
    main()
