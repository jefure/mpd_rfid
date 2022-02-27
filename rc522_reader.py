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
