#!/usr/bin/env python3

import RPi.GPIO as GPIO
import smbus
import time
import os
import subprocess
import logging

logging.basicConfig(filename='/home/pi/blank_hdmi.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s %(name)s %(message)s')

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.OUT, initial=1)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 175) # Initialize PWM on pwm Pin 18 with 175Hz frequency
BUS = 1
dc=50 # set dc variable to 0 for 0% duty cycle means lower value is brighter . allowed range is 0 ...100
pwm.start(dc) # Start PWM with 50% duty cycle
debug = False # debug mode (True or False)

input_state = GPIO.input(17)
# ---------------------------------
delay = 1800 # HDMI off after this time (in seconds) if no motion is detected
TSL2561_ADDR = 0x39

#create instance of I2C Object
i2cBus = smbus.SMBus(BUS)
# start measuring with 402 ms (scale factor 1)
i2cBus.write_byte_data(TSL2561_ADDR, 0x80, 0x03)

counter = delay
lasttimemotion = False

while True:
    input_state = GPIO.input(17)
    if input_state == True:
        if debug == True:
            print('motion!')
            logging.debug('motion detected')
        #else: logging.info('motion detected')
        counter = delay #reset counter
        if debug == True: print(counter)
        if lasttimemotion == False:
            #subprocess.call('vcgencmd display_power 1',shell=True)
            GPIO.output(27, 1)
            lasttimemotion = True
            if debug == True:
                print('Display on')
                logging.debug('Display on')
            else: logging.info('Display on')
    else:
        # no motion
        if debug == True:
            print('no motion detected')
            #logging.debug('no motion detected')
        #else: logging.info('no motion detected')
        counter = counter - 1
        if debug == True: print(counter)
        if lasttimemotion ==  True:
            if counter < 1:
                #subprocess.call('vcgencmd display_power 0',shell=True)
                GPIO.output(27, 0)
                lasttimemotion =  False
                if debug == True:
                    print('Display off')
                else: logging.info('Display off')
    if counter < 0:
        #prevent $counter from getting too small and negative overflow if no motion is detected for a very long time
        counter = 0
    # read brightness - least significant byte
    LSB = i2cBus.read_byte_data(TSL2561_ADDR, 0x8C)
    # read most significant byte
    MSB = i2cBus.read_byte_data(TSL2561_ADDR, 0x8D)
    Ambient = (MSB << 8) + LSB
    if debug == True: print("Ambient: {}".format(Ambient))
    # calculate duty cycle from ambient value
    if Ambient == 0: Ambient=1 # prevent division by zero
    dc = int(300/Ambient)
    if dc > 99: dc=100 # prevent dc values greater than 100 (allowed range is 0 ... 100)
    if debug == True: print("DC: {}".format(dc))
    pwm.ChangeDutyCycle(dc)
    time.sleep(1)
