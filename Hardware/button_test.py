import RPi.GPIO as GPIO
from time import sleep
button = 15

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(button, GPIO.IN)

while True:
    if GPIO.input(button):
        print("ON")
    else:
        print("OFF")
    sleep(0.1)
 