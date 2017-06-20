import RPi.GPIO as GPIO
import time
import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *

GPIO.setmode(GPIO.BOARD)
pin = 7 #input('Enter GPIO pin: ')
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
while True:
    input_state = GPIO.input(pin)
    if input_state == False:
        print('Button Pressed')
        GPIO.cleanup()
        unix('sudo reboot')
        break
    time.sleep(5)
    print(d2s('waiting for reboot command,',time.time()))
