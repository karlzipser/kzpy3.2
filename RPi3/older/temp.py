
import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31,GPIO.OUT)

pwm_steer = GPIO.PWM(31,50)

pwm_steer.start(0)

pwm_steer.ChangeDutyCycle(7.8)
pwm_steer.ChangeDutyCycle(0)
print('centered at 7.8 [?]')
time.sleep(3)

for nino in np.arange(2.5,8,0.2):
    pwm_steer.ChangeDutyCycle(nino)
    time.sleep(0.1);pwm_steer.ChangeDutyCycle(0);time.sleep(0.3)
    print nino
pwm_steer.ChangeDutyCycle(7.8)
time.sleep(0.3)
pwm_steer.ChangeDutyCycle(0)
GPIO.cleanup()


