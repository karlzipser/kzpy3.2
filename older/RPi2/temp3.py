
print("*** on RPi ****")
import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import RPi.GPIO as GPIO
EN1 = 7
IN1 = 12
IN2 = 13
out_pins = [EN1,IN1,IN2]


GPIO.setmode(GPIO.BOARD)
for p in out_pins:
	GPIO.setup(p,GPIO.OUT)

pwm_EN1 = GPIO.PWM(EN1,50)
pwm_EN1.start(0)
pwm_IN1 = GPIO.PWM(IN1,50)
pwm_IN1.start(0)
pwm_IN2 = GPIO.PWM(IN2,50)
pwm_IN2.start(0)



def forward(ds=50):
	pwm_IN1.ChangeDutyCycle(100)
	pwm_IN2.ChangeDutyCycle(0)
	pwm_EN1.ChangeDutyCycle(ds)

def reverse(ds=50):
	pwm_IN2.ChangeDutyCycle(100)
	pwm_IN1.ChangeDutyCycle(0)
	pwm_EN1.ChangeDutyCycle(ds)

def stop():
	pwm_IN2.ChangeDutyCycle(0)
	pwm_IN1.ChangeDutyCycle(0)
	pwm_EN1.ChangeDutyCycle(100)

def coast():
	pwm_IN2.ChangeDutyCycle(0)
	pwm_IN1.ChangeDutyCycle(0)
	pwm_EN1.ChangeDutyCycle(0)


#
##############

"""

# http://stackoverflow.com/questions/1093598/pyserial-how-to-read-the-last-line-sent-from-a-serial-device
import serial
ser = serial.Serial('/dev/tty.usbmodem1411',9600)
print ser.readline()
ser.write('5')

ser.flushInput()
while True:
	print ser.readline()

"""

