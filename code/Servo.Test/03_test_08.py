#! /usr/bin/python3 
import pigpio
from time import sleep

PIN = 8
MIN_PULSE_TIME = 500		# ms
MAX_TIME = 2500		# ms
LEAP = 1

SWEEP_TIME = 5000 	# ms

# connect to the 
pi = pigpio.pi()

steps = (MAX_PULSE_TIME-MIN_PULSE_TIME)/LEAP

wait_time = SWEEP_TIME / steps / 1000

pi.set_servo_pulsewidth(PIN, 0)    # off

# loop forever
while True:

    for period in range (MIN_PULSE_TIME, MAX_PULSE_TIME, LEAP):
        pi.set_servo_pulsewidth(PIN, period)
        sleep(wait_time)

    for period in range (MAX_PULSE_TIME, MIN_PULSE_TIME, -LEAP):
        pi.set_servo_pulsewidth(PIN, period)
        sleep(wait_time)
