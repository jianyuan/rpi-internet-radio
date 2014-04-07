#!/usr/bin/env python

from mpd import MPDClient
from Adafruit.CharLCD.Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
import RPi.GPIO as GPIO
import atexit
import re

# Config
SPEAKER_RELAY_CHANNEL = 11

# Set up Raspberry Pi GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKER_RELAY_CHANNEL, GPIO.OUT, initial=GPIO.HIGH)

# Set up LCD screen
lcd = Adafruit_CharLCD(pins_db=[23, 17, 27, 22])
lcd.begin(16, 2) # 16x2 LCD screen

# Set up MPD client
client = MPDClient()
client.connect('localhost', 6600)

def turn_on_speaker():
	GPIO.output(SPEAKER_RELAY_CHANNEL, GPIO.HIGH)

@atexit.register
def turn_off_speaker():
        GPIO.output(SPEAKER_RELAY_CHANNEL, GPIO.LOW)

@atexit.register
def mpd_disconnect():
	client.disconnect()

last_song = None
turn_on_speaker()

# Poll for current song
while True:
        current_song = client.currentsong()['title'].split(' - ', 2)

        if current_song != last_song:
                print 'Current song: ' + ' - '.join(current_song)
                lcd.clear()
                for line in current_song:
                        lcd.message(re.sub(r'([^\s\w]|_)+', '', line)[0:16] + '\n')
                last_song = current_song

        sleep(2)
