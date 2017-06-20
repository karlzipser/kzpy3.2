#! /usr/bin/python
#//anaconda/bin/python
#
import caffe
caffe.set_device(1)
caffe.set_mode_gpu()
from kzpy3.utils import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt
import os, serial, threading, Queue
import threading

img = zeros((94,168,3))
DO_LOADING = False
QUIT = False

def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver













if True:



	from kzpy3.vis import *
	MLK_pm_lat = 37.881556
	MLK_pm_lon = -122.278434
	miles_per_deg_lat = 68.94
	miles_per_deg_lon_at_37p88 = 54.41
	meters_per_mile = 1609.34
	b=load_obj(opjD('left_image_bound_to_data3')) #'/home/karlzipser/Desktop/temp_bag/caffe_z2_direct_local_sidewalk_test_data_03Nov16_18h33m09s_Mr_Orange/.preprocessed/left_image_bound_to_data3.pkl' )


	ts = sorted(b.keys())

	topics = ['gyro_heading_x','gyro_heading_y','gyro_heading_z',
	'gyro_x','gyro_y','gyro_z',
	'GPS2_lat','GPS2_long','GPS2_speed','GPS2_angle',
	'motor','steer','encoder',
	'acc_x','acc_y','acc_z','state']

	Data = {}
	for tp in topics:
		Data[tp] = []

	for t in ts:                                                                   
		Data['gyro_heading_x'].append(b[t]['gyro_heading'][0])
		Data['gyro_heading_y'].append(b[t]['gyro_heading'][1])
		Data['gyro_heading_z'].append(b[t]['gyro_heading'][2])
		Data['GPS2_lat'].append(b[t]['GPS2_lat'])
		Data['GPS2_long'].append(b[t]['GPS2_long'])
		Data['GPS2_speed'].append(b[t]['GPS2_speed'])
		Data['GPS2_angle'].append(b[t]['GPS2_angle'])
		Data['motor'].append(b[t]['motor'])
		Data['steer'].append(b[t]['steer'])
		Data['encoder'].append(b[t]['encoder'])
		Data['acc_x'].append(b[t]['acc'][0])
		Data['acc_y'].append(b[t]['acc'][1])
		Data['acc_z'].append(b[t]['acc'][2])
		Data['gyro_x'].append(b[t]['gyro'][0])
		Data['gyro_y'].append(b[t]['gyro'][1])
		Data['gyro_z'].append(b[t]['gyro'][2])
		Data['state'].append(b[t]['state'])

	for tp in topics:
		Data[tp] = na(Data[tp])

	Data['meters_y'] = (Data['GPS2_lat']-MLK_pm_lat)*miles_per_deg_lat*meters_per_mile
	Data['meters_x'] = (Data['GPS2_long']-MLK_pm_lon)*miles_per_deg_lon_at_37p88*meters_per_mile

	hx = Data['gyro_heading_x']
	hy = Data['gyro_heading_y']
	hz = Data['gyro_heading_z']
	hdx=0*hx;hdy=0*hy;hdz=0*hz
	for i in range(1+5*30,len(hx),1):
	    hdx[i] =  hx[i]-hx[(i-5*30):(i-4*30)].mean()
	    hdy[i] =  hy[i]-hy[(i-5*30):(i-4*30)].mean()
	    hdz[i] =  hz[i]-hz[(i-5*30):(i-4*30)].mean()
	Data['d_gyro_heading_x'] = hdx
	Data['d_gyro_heading_y'] = hdy
	Data['d_gyro_heading_z'] = hdz

	"""
	zData = {}
	for tp in ['acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z',
		'd_gyro_heading_x','d_gyro_heading_y','d_gyro_heading_z']:
		zData[tp] = zscore(Data[tp],3)
	zData['meters_x'] = Data['meters_x']/10.0
	zData['meters_y'] = Data['meters_y']/10.0
	zData['state'] = Data['state'].copy()
	for i in range(len(zData['state'])):
		if int(zData['state'][i]) in [5,7]:
			zData['state'][i] = 1
		else:
			zData['state'][i] = 0
	zData['motor'] = (Data['motor']-49.)/10.
	zData['steer'] = zscore(Data['steer'],3)
	zData['encoder'] = Data['encoder']/3.
	"""
	zData = {}

	zData['meters_x'] = Data['meters_x']/10.0
	zData['meters_y'] = Data['meters_y']/10.0
	zData['state'] = Data['state'].copy()
	for i in range(len(zData['state'])):
		if int(zData['state'][i]) in [5,7]:
			zData['state'][i] = 1
		else:
			zData['state'][i] = 0
	#zData['motor'] = (Data['motor']-49.)/10.
	#zData['steer'] = zscore(Data['steer'],3)
	zData['encoder'] = Data['encoder']/3.-2.0
	zData['GPS2_angle'] = (Data['GPS2_angle']-150)/360.
	img = zeros((len(zData.keys()),len(zData['state'])))
	topics = sorted(zData.keys())
	ctr = 0
	for tp in topics:
		img[ctr,:] = zData[tp]
		ctr += 1
	"""
	for i in range(20000,60000,2):
		input_img = img[:,i-150:i]
		mi(input_img)
		plt.pause(0.001)
		steer_target = []
		motor_target = []
		for j in range(i,i+10):
			if zData['state'][j] == 1:
				steer_target.append(int(Data['steer'][j]))
				motor_target.append(int(Data['motor'][j]))
			else:
				steer_target.append(49)
				motor_target.append(49)
		print steer_target
		print motor_target
		print "---"
	"""







unix('mkdir -p '+opjD('g0'))

solver_file_path = opjh("kzpy3/caf3/g0/solver.prototxt")
solver = setup_solver()
weights_file_path = most_recent_file_in_folder(opjD('g0'),['g0','caffemodel']) 
if weights_file_path == "None":
	weights_file_path = None
if weights_file_path != None:
	print "loading " + weights_file_path
	solver.net.copy_from(weights_file_path)




def array_to_int_list(a):
	l = []
	for d in a:
		l.append(int(d*100))
	return l



t0 = time.time()
if True:
	while True:
		skip = False
		i = randint(20000,60000)
		input_img = img[:,i-150:i]
		steer_target = []
		motor_target = []
		for j in range(i,i+30):
			if int(Data['state'][j]) in [2,4]:
				skip = True
				continue
			#print d2s('here',Data['motor'][j])
			if Data['motor'][j] < 49:
				skip = True
			if zData['state'][j] == 1:
				steer_target.append(int(Data['steer'][j]))
				motor_target.append(int(Data['motor'][j]))
			else:
				steer_target.append(49)
				motor_target.append(49)
		#print steer_target
		#print motor_target
		if not skip:
			if Data['motor'][-1] > 48:
				solver.net.blobs['input_data'].data[0,0,:,:] = input_img.copy()
				solver.net.blobs['steer_motor_target_data'].data[0,:] = na(steer_target+motor_target)/100.
				#print steer_target+motor_target
				#print solver.net.blobs['steer_motor_target_data'].data
				assert(solver.net.blobs['steer_motor_target_data'].data[0,59]>40/100.)
				solver.net.blobs['steer_motor_target_data'].data[0,30:69] = 49/100.
				solver.step(1)
				if time.time()-t0 >3:
					if int(steer_target[9]) != 49:
						t0 = time.time()
						figure(2)
						clf()
						plot(array_to_int_list(solver.net.blobs['steer_motor_target_data'].data[0,:]),'o-')
						plot(array_to_int_list(solver.net.blobs['ip2'].data[0,:]),'x-')
						plt.ylim(0,99)
						plot([0,60],[49,49],'r')
						#print "---"
						mi(input_img,1)
						plt.pause(0.001)