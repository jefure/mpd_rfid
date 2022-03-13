# MPD RFID Controller

Python project to create a controller for a mpd server to play playlists selected by rfid tags.

Licensing
---------
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

The source code is licensed using the GNU GPLv3 see LICENSE.md

## Overview

A raspberry zero w with a rc522 rfid reader is used to play predefined playlists on a mpd server.
The mpd server runs on a separate server where the music is stored. This server is connected to loudspeakers.

### Hardware

Connecting the raspberry to the rc522 module:

| RF522 Modul | Raspberry Pi |
| ----------- | ------------ |
| SDA | Pin 24 / GPIO8 (CE0) |
| SCK | Pin 23 / GPIO11 (SCKL) |
| MOSI | Pin 19 / GPIO10 (MOSI) |
| MISO | Pin 21 / GPIO9 (MISO) |
| IRQ | — |
| GND | Pin6 (GND) |
| RST | Pin22 / GPIO25 |
| 3.3V | Pin 1 (3V3) |

### Code

- mpd_handler.py Lib to interact with the mpd server
- playlist_manager.py Script to fill the database with playlist data
- rc522_reader.py Lib to interact with the rfid reader
- repository.py Lib to interact with te sqlite database
- rfid_mpd_controller.py The script that reads the rfid and plays the selected playlist using the mpd server
- rfid_tag_playlist_manager.py Script to link a rfid with a playlist
- web.py A flask web application to create the cover images