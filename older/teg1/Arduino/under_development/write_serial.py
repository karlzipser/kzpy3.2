import serial
import time
from kzpy3.utils import *

ser = serial.Serial('/dev/tty.usbmodem1421',baudrate=115200, timeout=100)

print "Go!"

#for i in range(256):
#	print time.time()
ser.write('1')
#	print time.time()
print ser.readline()

a=raw_input('raw_input')

t0 = time.time()
for j in range(16):
	print j
	for i in range(16):
		ser.write('('+str(i)+')')
		print d2s(j,')',ser.readline())
print time.time()-t0