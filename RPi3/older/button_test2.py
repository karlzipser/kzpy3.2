import RPi.GPIO as GPIO
import time
import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *

GPIO.setmode(GPIO.BOARD)
pin = input('Enter GPIO pin: ')
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button_press = 0

def my_callback(channel):
	global button_press
	if GPIO.input(pin): 
		print "Rising edge detected"  
	else:
		print "Falling edge detected" 
		button_press += 1

# when a changing edge is detected on port 25, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback)  

while button_press < 5:
    print(time.time())
    time.sleep(1)