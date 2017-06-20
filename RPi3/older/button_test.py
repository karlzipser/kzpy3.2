import RPi.GPIO as GPIO
import time
import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *

GPIO.setmode(GPIO.BOARD)
pin = input('Enter GPIO pin: ')
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
while True:
    input_state = GPIO.input(pin)
    if input_state == False:
        print('Button Pressed')
        GPIO.cleanup()
        #unix('sudo shutdown -h -P 0')
        break
    time.sleep(0.1)
    print(time.time())
