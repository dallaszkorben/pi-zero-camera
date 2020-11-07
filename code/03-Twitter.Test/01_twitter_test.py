#! /usr/bin/python3 
import pigpio
import picamera
from time import sleep
from twython import Twython

C_KEY = "70tK0g2knsWil9z5ajLIcYzQY"
C_SECRET = "hLOCn052z6Pha11zoFu8B5A2IcZW68TEHBwXyfrWjZXlpfW9CP"
A_TOKEN = "1297204667143921665-GFCCTBc2qwII8Py6AcHIk4Wid7TQ8O"
A_SECRET = "x8sMPbpHTGpWeajB4mvUVuovqkwV2ItNvFW3cFaOk2ujr"

api = Twython(C_KEY, C_SECRET, A_TOKEN, A_SECRET)

position = {}
position['1'] = (0,0)
position['2'] = (-90,0)
position['3'] = (90,-45)
position['4'] = (25,60)
position['5'] = (-45,-90)

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

FILE_NAME = 'pict.jpg'

# connect to camera
camera = picamera.PiCamera()

# connect to the pigpio
pi = pigpio.pi()

pi.set_servo_pulsewidth(PIN_HORIZONTAL, 0)    # off
pi.set_servo_pulsewidth(PIN_VERTICAL, 0)    # off

def con_horizontal_degree_to_pulse(degree):
    rel = (degree - MIN_HORIZONTAL_DEGREE)/(MAX_HORIZONTAL_DEGREE-MIN_HORIZONTAL_DEGREE)
    pulse = MIN_PULSE_HORIZONTAL + rel * (MAX_PULSE_HORIZONTAL - MIN_PULSE_HORIZONTAL)
    return pulse

def con_vertical_degree_to_pulse(degree):
    rel = (degree - MIN_VERTICAL_DEGREE)/(MAX_VERTICAL_DEGREE-MIN_VERTICAL_DEGREE)
    pulse = MIN_PULSE_VERTICAL + rel * (MAX_PULSE_VERTICAL - MIN_PULSE_VERTICAL)
    return pulse




# loop forever
try:
    while True:
        pos = input("Enter Positions (1-9):")
        if pos in position:

            # --- Move the Camera ---
            print(position[pos][0], position[pos][1])
            hor_pulse = con_horizontal_degree_to_pulse(position[pos][0])
            ver_pulse = con_vertical_degree_to_pulse(position[pos][1])

            pi.set_servo_pulsewidth(PIN_HORIZONTAL, hor_pulse)
            pi.set_servo_pulsewidth(PIN_VERTICAL, ver_pulse)

            # --- Take picture ---
            sleep(1)
            camera.capture(FILE_NAME)

            # --- Tweet the picture ---
            image_open = open(FILE_NAME, 'rb')
            response = api.upload_media(media=image_open)

            api.update_status(status='Message with photo', media_ids=[response['media_id']])


except KeyboardInterrupt:
    print("CTRL-C: Terminating program.")
finally:
    print("Done...")


