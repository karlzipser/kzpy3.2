import RPi.GPIO as GPIO
import time
import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *

GPIO.setmode(GPIO.BOARD)
pin = 23 #input('Enter GPIO pin: ')
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

reed_close = 0

start_time = 0

rps = 0

def my_callback(channel):
	global reed_close
	global start_time
	global rps
	if GPIO.input(pin): 
		pass #print "Rising edge detected"  
	else:
		#print "Falling edge detected" 
		reed_close += 1
		"""
		if start_time == 0:
			start_time = time.time()
		if reed_close == 5: #time.time() -  start_time > 1:
			rps = reed_close / (time.time() - start_time)
			start_time = time.time()
			reed_close = 0
		"""
# when a changing edge is detected on port 25, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback)  



def cleanup_and_exit():
    GPIO.cleanup()
    print(os.path.basename(sys.argv[0])+' : cleaned up.')
    time.sleep(1)
    sys.exit()

reed_close_10s = 0
reed_close_lst = []
try:
    while True:
		reed_close = 0
		start_t = time.time()

		time.sleep(1)

		d_time = time.time() - start_t
		if len(reed_close_lst) < 2:
			reed_close_lst.append((reed_close,d_time))
		else:
			advance(reed_close_lst,(reed_close,d_time))
		cnt = 0
		dt = 0
		for r in reed_close_lst:
			cnt += r[0]
			dt += r[1]
		print cnt / dt
		#print reed_close, reed_close_lst
except KeyboardInterrupt:
    cleanup_and_exit()



