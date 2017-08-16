import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

# tested 7 13 15 19 21 23 29 [31,33,35 not tested ] 37

def test_pin(p):	
	GPIO.setup(p,GPIO.OUT)
	for i in range(5):
		GPIO.output(p, True)
		time.sleep(1/40.0)		
		GPIO.output(p, False)
		time.sleep(1/2.0)
