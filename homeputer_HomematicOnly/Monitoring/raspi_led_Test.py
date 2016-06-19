#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep

# Needs to be BCM. GPIO.BOARD lets you address GPIO ports by periperal
# connector pin number, and the LED GPIO isn't on the connector
GPIO.setmode(GPIO.BCM)

GPIO.cleanup()
# set up GPIO output channel
GPIO.setup(2, GPIO.OUT) #gelbes led, 2 pin von oben, innere Reihe
GPIO.setup(3, GPIO.OUT) #grünes led, 3 pin von oben, innere Reihe
# On
GPIO.output(3, GPIO.LOW)

# Wait a bit
sleep(3)

# Off
GPIO.output(3, GPIO.HIGH)

while True:
      GPIO.output(2, GPIO.LOW) # gelbes LED an, 2 pin von oben innen, GPIO 03
      sleep(0.1)
      GPIO.output(2, GPIO.HIGH)
      sleep(1)
