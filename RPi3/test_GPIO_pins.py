import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

# see http://pinout.xyz/pinout/pin7_gpio4 for guide to pins
# tested 7 13 15 19 21 23 29 [31,33,35 not tested ] 37
# pin 11 dead.

def test_pin(p):	
	GPIO.setup(p,GPIO.OUT)
	ready = raw_input('ready?')
	for i in range(5):
		GPIO.output(p, True)
		time.sleep(1/40.0)		
		GPIO.output(p, False)
		time.sleep(1/2.0)

if __name__ == '__main__':
	pin = input('Enter GPIO pin: ')
	test_pin(pin)
	GPIO.cleanup()
