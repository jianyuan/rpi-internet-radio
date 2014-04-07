#!/usr/bin/env python

from mpd import MPDClient
from Adafruit.CharLCD.Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
import RPi.GPIO as GPIO
import atexit
import re
import sys
import os

# Config
SPEAKER_RELAY_CHANNEL = 11
SHUTDOWN_BUTTON_CHANNEL = 9
SHUTDOWN_BUTTON_PRESS_DURATION = 5

# Set up Raspberry Pi GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKER_RELAY_CHANNEL, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(SHUTDOWN_BUTTON_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
shutdown_button_active_duration = 0

turn_on_speaker()

# Poll for current song
while True:
	if GPIO.input(SHUTDOWN_BUTTON_CHANNEL):
		shutdown_button_active_duration += 1

		if shutdown_button_active_duration >= SHUTDOWN_BUTTON_PRESS_DURATION:
			turn_off_speaker()
			os.system('sudo shutdown -h now')
			sys.exit()
	else:
		shutdown_button_active_duration = 0

        current_song = client.currentsong()['title'].split(' - ', 2)

        if current_song != last_song:
                print 'Current song: ' + ' - '.join(current_song)
                lcd.clear()
                for line in current_song:
                        lcd.message(re.sub(r'([^\s\w]|_)+', '', line)[0:16] + '\n')
                last_song = current_song

        sleep(2)
