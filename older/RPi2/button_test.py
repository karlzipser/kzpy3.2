import RPi.GPIO as GPIO
import time
import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
while True:
    input_state = GPIO.input(7)
    if input_state == False:
        print('Button Pressed')
        GPIO.cleanup()
        unix('sudo shutdown -h -P 0')
        break
    time.sleep(0.1)
    print(time.time())
