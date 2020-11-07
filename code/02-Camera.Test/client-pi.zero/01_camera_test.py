#! /usr/bin/python3 
import picamera
from time import sleep
import requests

# connect to the pigpio
camera = picamera.PiCamera()

FILE_NAME = "pict.jpg"
SERVER = "192.168.1.30"

# loop forever
while True:

    camera.capture(FILENAME)

    with open(FILENAME, 'rb') as f:
        r = requests.post('http://' + SERVER + '/post', files={FILENAME: f})

    sleep(8)


