#!/usr/bin/env python3
#
# Switch HDMI port of Raspberry Pi triggered by a motion sensor attached to GPIO pin 17 on and off
# I've used a cheap radar sensor HFS-DC06. It has a adjustable sensitivity and output timer
# since this script checks every second the input status, the motion sensor must have a minimum 
# 'on' time of 1.1 seconds at the output (2 seconds in my case working great)
# I use this for a picture frame and a wall-mounted touchscreen

import RPi.GPIO as GPIO
import time
import os
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
input_state = GPIO.input(17)

delay = 1800 # HDMI off after this time (in seconds) if no motion is detected
debug = False # debug mode (True or False)
counter = delay
lasttimemotion = False

while True:
    input_state = GPIO.input(17)
    if input_state == True:
        if debug == True: print('motion!')
        counter = delay #reset counter
        if debug == True: print(counter)
        if lasttimemotion == False:
            subprocess.call('vcgencmd display_power 1',shell=True)
            lasttimemotion = True
            if debug == True: print('switch HDMI on')
    else:
        # no motion
        if debug == True: print('no motion')
        counter = counter - 1
        if debug == True: print(counter)
        if lasttimemotion ==  True:
            if counter < 1:
                subprocess.call('vcgencmd display_power 0',shell=True)
                lasttimemotion =  False
                if debug == True: print('switch HDMI off')
    if counter < 0:
        #prevent $counter from getting too small and negative overflow if no motion is detected for a long time
        counter = 0
    time.sleep(1)
