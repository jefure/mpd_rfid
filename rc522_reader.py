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
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


def read_rfid():
    reader = SimpleMFRC522()
    try:
        print('Put RFID tag on the reader')
        rfid, text = reader.read()
        print('Got id: ', rfid)
        return rfid
    finally:
        cleanup()


def cleanup():
    GPIO.cleanup()
