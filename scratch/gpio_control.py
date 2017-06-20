import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import RPi.GPIO as GPIO
import Tkinter as tk
#import time
"""
d = 7.15
pwm = GPIO.PWM(40,50);pwm.start(d);time.sleep(0.1);pwm.stop()


VNC
on RPi,
	tightvncserver
	vncserver :0 -geometery 1920x1080 -depth 24
may need to adust the vncserver number.

Then on Mac: open vnc://pi@192.168.43.20:5901

"""

SERVO_IN = 38
MOTOR_IN = 40
#HB_EN1 = 7
#HB_IN1 = 12
#HB_IN2 = 13

out_pins = [SERVO_IN,MOTOR_IN]#[SERVO_IN, HB_EN1, HB_IN1, HB_IN2]

GPIO.setmode(GPIO.BOARD)
for p in out_pins:
	GPIO.setup(p,GPIO.OUT)

def do_pwm(pin,frequency,duration,duty_cycle):
	pwm = GPIO.PWM(pin,frequency)
	start_time = time.time()
	pwm.start(duty_cycle)
	while time.time() < start_time + duration:
		pass;
	pwm.stop()
"""
def motor(
	duty_cycle=10,
	durataion=0.5,
	freqency=100,
	pin=HB_EN1,
	initial_pulse_time=0.1):
	do_pwm(pin,frequency,initial_pulse_time,100)
	do_pwm(pin,frequency,durataion-initial_pulse_time,duty_cycle)
"""
def servo(
	duty_cycle=7.5,
	durataion=0.2,
	freqency=50,
	pin=SERVO_IN):
	"""
	"""
	do_pwm(pin,frequency,duration,duty_cycle)




def onKeyPress(event):
    text.insert('end', '%s ' % (event.char, ))
    if event.char == '1':
        do_pwm(38,50,0.3,7.8)
    if event.char == '2':
        do_pwm(38,50,0.3,9.5)
    if event.char == '3':
        do_pwm(38,50,0.3,11)
    if event.char == '4':
        do_pwm(40,50,0.3,7.20)
    if event.char == '5':
        do_pwm(40,50,0.3,7.18)
    if event.char == 'q':
        GPIO.cleanup()
        root.destroy() #root.quit()

root = tk.Tk()
root.geometry('300x200')
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
root.bind('<KeyPress>', onKeyPress)
root.mainloop()



