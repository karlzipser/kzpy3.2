#!/usr/bin/env python
"""
An animated image
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from kzpy3.teg2.data.access.get_data_from_bag_files5 import *
from kzpy3.vis import *
fig = plt.figure(1)

p = '/home/karlzipser/Desktop/bair_car_data_min_disks/bair_car_data_6_min/caffe_z2_direct_local_sidewalks_09Oct16_08h30m15s_Mr_Orange'
L = load_obj(opj(p,'.preprocessed/left_image_bound_to_data2.pkl'))
#P = load_obj('/home/karlzipser/Desktop/bair_car_data_min_disks/bair_car_data_6_min/direct_local_sidewalks_25Sep16_17h59m02s_Mr_Orange/.preprocessed/bair_car_2016-09-25-18-28-17_50.bag.pkl')

B = Bag_Folder2(p)
B.load_all_bag_files()

ctr = 0
skip = 0
shown = 0.0

ts = sorted(B.img_dic.keys())
imgs = []
for t in ts:
	imgs.append(B.img_dic[t]/255.)
t0 = time.time()
steers = list(49+zeros(20))
motors = list(49+zeros(20))
encoders = list(zeros(20))
gyros = []
accs = []
def updatefig(*args):
	try:
		global ctr, shown, skip
		while ts[ctr]-ts[0]<time.time()-t0:
			ctr += 1
			skip += 1
			steers.append(L[ts[ctr]]['steer'])
			motors.append(L[ts[ctr]]['motor'])
			encoders.append(L[ts[ctr]]['encoder'])
			gyros.append(L[ts[ctr]]['gyro'])
			accs.append(L[ts[ctr]]['acc'])
			
		shown=shown+1
		print d2s('skip/shown =', ctr/shown)
		mi(imgs[ctr],1,[3,2,1])
		
		plt.subplot(3,2,5)
		gyros.append(L[ts[ctr]]['gyro'])

		#try:
		if ctr > 20:
			plt.plot(np.array(gyros[-20:])[:,0],range(0,20))
			plt.plot(np.array(gyros[-20:])[:,1],range(0,20))
			plt.plot(np.array(gyros[-20:])[:,2],range(0,20))
			plt.ylim((0,20))
			plt.xlim((-100,100))
			plt.subplot(3,2,6)
		accs.append(L[ts[ctr]]['acc'])
		if ctr > 20:
			plt.plot(np.array(accs[-20:])[:,0],range(0,20))
			plt.plot(np.array(accs[-20:])[:,1],range(0,20))
			plt.plot(np.array(accs[-20:])[:,2],range(0,20))
			plt.ylim((0,20))
			plt.xlim((-20,20))	#except:
		#	pass


		plt.subplot(3,2,2)
		steers.append(L[ts[ctr]]['steer'])
		plt.plot(99-np.array(steers[-20:]),range(20))
		plt.ylim((0,20))
		plt.xlim((-5,105))
		
		plt.subplot(3,2,3)
		motors.append(L[ts[ctr]]['motor'])
		plt.plot(np.array(motors[-20:]),range(20))
		plt.ylim((0,20))
		plt.xlim((-5,105))

		plt.subplot(3,2,4)
		encoders.append(L[ts[ctr]]['encoder'])
		plt.plot(np.array(encoders[-20:]),range(20))
		plt.ylim((0,20))
		plt.xlim((-1,10))
	except:
		print 'error'
	

ani = animation.FuncAnimation(fig, updatefig, interval=1)#, blit=True)

plt.show()