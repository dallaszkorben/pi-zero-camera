#! /usr/bin/python3 
import re
import pigpio
import picamera
from time import sleep
from twython import Twython
from twython import TwythonStreamer
import configparser


C_KEY = "70tK0g2knsWil9z5ajLIcYzQY"
C_SECRET = "hLOCn052z6Pha11zoFu8B5A2IcZW68TEHBwXyfrWjZXlpfW9CP"
A_TOKEN = "1297204667143921665-GFCCTBc2qwII8Py6AcHIk4Wid7TQ8O"
A_SECRET = "x8sMPbpHTGpWeajB4mvUVuovqkwV2ItNvFW3cFaOk2ujr"

#position = {}
#position['1'] = (0,0)
#position['2'] = (-90,0)
#position['3'] = (90,-45)
#position['4'] = (25,60)
#position['5'] = (-45,-90)

PIN_VERTICAL = 18
MIN_PULSE_VERTICAL = 500		# ms
MAX_PULSE_VERTICAL = 2500		# ms

PIN_HORIZONTAL = 8
MIN_PULSE_HORIZONTAL = 500		# ms
MAX_PULSE_HORIZONTAL = 2500		# ms

MIN_HORIZONTAL_DEGREE = -90
MAX_HORIZONTAL_DEGREE = 90

MIN_VERTICAL_DEGREE = -90
MAX_VERTICAL_DEGREE = 90

FILE_NAME = "pict.jpg"
USER_NAME = "akoel3"
POS_KEY_WORD = "poz" 
CONFIG_FILE_NAME = "positions.ini"

# config file
config = configparser.ConfigParser()
config.read(CONFIG_FILE_NAME)

position = {}
for option in config.options("main"):
    value = config.get("main", option)
    values = value.split(",")
    position[option]=(int(values[0]),int(values[1]))

# connect to Twitter
api = Twython(C_KEY, C_SECRET, A_TOKEN, A_SECRET)

# connect to camera
camera = picamera.PiCamera()

# connect to the pigpio
pi = pigpio.pi()

pi.set_servo_pulsewidth(PIN_HORIZONTAL, 0)    # off
pi.set_servo_pulsewidth(PIN_VERTICAL, 0)    # off



class MyStreamer(TwythonStreamer):

    def con_horizontal_degree_to_pulse(self, degree):
        rel = (degree - MIN_HORIZONTAL_DEGREE)/(MAX_HORIZONTAL_DEGREE-MIN_HORIZONTAL_DEGREE)
        pulse = MIN_PULSE_HORIZONTAL + rel * (MAX_PULSE_HORIZONTAL - MIN_PULSE_HORIZONTAL)
        return pulse

    def con_vertical_degree_to_pulse(self, degree):
        rel = (degree - MIN_VERTICAL_DEGREE)/(MAX_VERTICAL_DEGREE-MIN_VERTICAL_DEGREE)
        pulse = MIN_PULSE_VERTICAL + rel * (MAX_PULSE_VERTICAL - MIN_PULSE_VERTICAL)
        return pulse

    def on_success(self, data):
        if data['user']['screen_name'] == USER_NAME and 'text' in data:

            # filter out the position (if it is the right message starting with "POS" following with numbers
            m = re.search(POS_KEY_WORD + ' (\d+)', data['text'])
            pos = m.group(1) if m != None else ""

            if pos in position:

                # --- Move the Camera ---
                print("Position: ", position[pos][0], position[pos][1])

                hor_pulse = self.con_horizontal_degree_to_pulse(position[pos][0])
                ver_pulse = self.con_vertical_degree_to_pulse(position[pos][1])

                pi.set_servo_pulsewidth(PIN_HORIZONTAL, hor_pulse)
                pi.set_servo_pulsewidth(PIN_VERTICAL, ver_pulse)

                # --- Take picture ---
                sleep(1)
                camera.capture(FILE_NAME)

                # --- Tweet the picture ---
                image_open = open(FILE_NAME, 'rb')
                response = api.upload_media(media=image_open)

                api.update_status(status='Message with photo', media_ids=[response['media_id']])

stream = MyStreamer(C_KEY, C_SECRET, A_TOKEN, A_SECRET)
stream.statuses.filter(track=POS_KEY_WORD)

