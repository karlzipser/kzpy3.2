#!//anaconda/bin/python #/usr/bin/env python
import serial
from kzpy3.vis import *

ser = serial.Serial('/dev/cu.usbmodem1461', 250000)
read_byte = ser.read()

t0 = time.time()
ctr = 0
D = 64
A = np.zeros((D**2,1),'uint8')
while read_byte is not None:
	#print int(read_byte.encode('hex'), 16)
	read_byte = ser.read()
	if int(read_byte.encode('hex'), 16) == 255:
		ser.write('(69)')
		ctr += 1
		for i in range(D**2):
			#if np.mod(i,100) == 1:
			#	print i
			read_byte = ser.read()
			read_int = int(read_byte.encode('hex'), 16)
			#print read_int
			A[i] = read_int*4
		t1 = time.time()
		print (ctr,int(read_byte.encode('hex'), 16), t1-t0)
		t0 = t1
		B = np.reshape(A,(D,D));
		mi(B)
		plt.pause(0.00001)