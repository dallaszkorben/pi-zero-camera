#! /usr/bin/python3 
import pigpio
from time import sleep

PIN = 18

# connect to the 
pi = pigpio.pi()

pi.set_servo_pulsewidth(PIN, 0)    # off

try:
    while True:
        pulse_time = float(input("Enter Pulse Time (Left = 500 to Right = 2500):"))
        pi.set_servo_pulsewidth(PIN, pulse_time)

except KeyboardInterrupt:
    print("CTRL-C: Terminating program.")
finally:
    print("Done...")
