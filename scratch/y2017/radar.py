"""
8 January 2017
Code to sample from Eagle RFBeam radar
"""

from kzpy3.vis import *
from socket import *
import struct
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12345))



def get_Eagle_RFBeam_ADC_arrays():
	raw_data_list = []
	chirps = ['no','nope']
	timer = Timer(1.)
	while True:
		assert(not timer.check())
		data, address = serverSocket.recvfrom(1069)
		raw_data_list.append(data[3:])
		chirps.append(struct.unpack('b', data[2])[0])
		if chirps[-1] == chirps[-2]:
			raw_data_list = raw_data_list[-2:]
			break
	chirps = chirps[-2:]
	assert(chirps[0] == chirps[1])
	assert(len(raw_data_list) == 2)

	t0 = time.time()
	data_list = [[],[],[],[]]

	for i in range(2):
		raw_data_list[i] = [raw_data_list[i][:512],raw_data_list[i][512:]]

	ctr = 0
	for i in range(2):
		for j in range(2):
			for k in range(0,len(raw_data_list[i][j]),2):
				b = raw_data_list[i][j][k]
				c = struct.unpack('b', b)[0]
				data_list[2*i+j].append(c)
	for i in range(4):
		assert(len(data_list[i]) == 256)
	assert(time.time()-t0) < 1.5/(10.**3)
	return array(data_list)






import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack






timer = Timer(60*5)
timer2 = Timer(0.1)
#img = zeros((256,256))+1.
#img2 = zeros((256,256))
#img3 = []
while not timer.check():
	d = get_Eagle_RFBeam_ADC_arrays()
	#img3.append(d[0,:])
	#for i in range(len(d[0])):
	#	img2[d[0][i]+128,d[2][i]+128] += 1
	#img += img2
	if timer2.check():
		figure(1)
		clf()
		if True:
			if False:
				L,H = -128,128
				plt.axis((L,H,L,H))
				plot(d[0,:],d[2,:],'o')
				plot(d[1,:],d[3,:],'x')
			else:
				"""
				L2,H2 = 0,256
				L1,H1 = -128,128
				plt.axis((L2,H2,L1,H1))
				plot(d[0,:],'o')
				plot(d[1,:],'o')
				plot(d[2,:],'x')
				plot(d[3,:],'x')
				"""

			# Number of samplepoints
			N = 256
			# sample spacing
			T = 1.0 / 800.0
			x = np.linspace(0.0, N*T, N)
			y = d[0,:]
			yf = scipy.fftpack.fft(y)
			xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

			plot(xf, 2.0/N * np.abs(yf[:N//2]))

			
			#mi(img2/img,2)

		#if len(img3) >= 256:
		#	mi(array(img3)[-256:,:],'img3')
		#img2 *= 0
		pause(0.0000001)
		timer2.reset()


"""
d=[]
for k in range(0,len(r1),2):
	a = struct.unpack_from('b', r1,k)[0]
	b = struct.unpack_from('b', r1,k+1)[0]
	d.append(a)#128*a+0*b)
figure(1)
#clf()
plot(d)
"""



"""
# http://stackoverflow.com/questions/21542194/power-spectrum-of-real-data-with-fftpack-on-log-axis

import pyfits
import numpy as np
from scipy.fftpack import fft, rfft, fftfreq
import pylab as plt

x,y = np.loadtxt('data.txt', usecols = (0,1), unpack=True)
y = y - y.mean()

W = fftfreq(y.size, d=(x[1]-x[0])*86400)
plt.subplot(2,1,1)
plt.plot(x,y)
plt.xlabel('Time (days)')

f_signal = fft(y)
plt.subplot(2,1,2)
plt.plot(W, abs(f_signal)**2)
plt.xlabel('Frequency (Hz)')

plt.xscale('log')
plt.xlim(10**(-6), 10**(-5))
plt.show()

"""
