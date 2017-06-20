#! /usr/bin/python
#//anaconda/bin/python

import caffe
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files2 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt


########################################################
#          SETUP SECTION
#
solver_file_path = opjh("kzpy3/caf3/z1/solver.prototxt")
weights_file_path = opjD('z1/z1_iter_510000.caffemodel') #
#
########################################################




def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver



img = zeros((94,168,3))#,'uint8')
def load_data_into_model(solver,data):
	global img
	if data == 'END' :
		print """data = 'END':"""
		return False
	if 'left' in data:
		if type(data['left'][0]) == np.ndarray:
			target_data = data['steer']
			target_data += data['motor']

			solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = data['left'][0][:,:]/255.0-.5
			solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = data['left'][1][:,:]/255.0-.5
			solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = data['right'][0][:,:]/255.0-.5
			solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = data['right'][1][:,:]/255.0-.5

				
				#mi(solver.net.blobs['ZED_data_pool2'].data[0,0,:,:],'left')
				#mi(solver.net.blobs['ZED_data_pool2'].data[0,2,:,:],'right')


			for i in range(len(target_data)):
				solver.net.blobs['steer_motor_target_data'].data[0,i] = target_data[i]/99.

		else:
			print """not if type(data['left']) == np.ndarray: """+str(time.time())
	else:
		pass #print """not if 'left' in data: """+str(time.time())
		return 'no data'
	return True

# 
#
loss_timer = time.time()
loss = []
def run_solver(solver, bair_car_data, num_steps):
	if time.time() - loss_timer > 60*15:
		save_obj(loss,opjD('z1','loss'))
	global img
	global loss
	step_ctr = 0
	ctr = 0
	while step_ctr < num_steps:
		imshow = False
		if np.mod(ctr,20) == 0:
			imshow = True
		result = load_data_into_model(solver, bair_car_data.get_data(['steer','motor'],10,2))
		if result == False:
			break
		if result == True:
			solver.step(1)
			a = solver.net.blobs['steer_motor_target_data'].data[0,:] - solver.net.blobs['ip2'].data[0,:]
			loss.append(np.sqrt(a * a).mean())
			ctr += 1

			if imshow:
				print (ctr,np.array(loss[-99:]).mean())
				img[:,:,0] = solver.net.blobs['ZED_data_pool2'].data[0,0,:,:]
				img += 0.5
				img *= 255.
				img[:,:,1] = img[:,:,0]
				img[:,:,2] = img[:,:,0]
				cv2.imshow('left',img.astype('uint8'))
				#cv2.imshow('right',solver.net.blobs['ZED_data_pool2'].data[0,2,:,:])
				"""
				img[:,:,0] = solver.net.blobs['ZED_data_pool2'].data[0,2,:,:]
				img[:,:,1] = img[:,:,0]
				img[:,:,2] = img[:,:,0]
				cv2.imshow('right',img)
				#cv2.imshow('right',solver.net.blobs['ZED_data_pool2'].data[0,2,:,:])
				"""
				if cv2.waitKey(1) & 0xFF == ord('q'):
				    pass
				print np.round(solver.net.blobs['steer_motor_target_data'].data[0,:][:3],3)
				print np.round(solver.net.blobs['ip2'].data[0,:][:3],3)
		step_ctr += 1

#if __name__ == '__main__':

unix('mkdir -p '+opjD('z1'))
#bair_car_data = Bair_Car_Data('/home/karlzipser/Desktop/bair_car_data/',1000,100)
bair_car_data = Bair_Car_Data('/Volumes/temp/bair_car_data/',1000,100)

#caffe.set_device(0)
#caffe.set_mode_gpu()
solver = setup_solver()

if weights_file_path != None:
	print "loading " + weights_file_path
	solver.net.copy_from(weights_file_path)
while True:
	try:
		run_solver(solver,bair_car_data,3000)
	except Exception as e:
		print "***************************************"
		print e.message, e.args
		print "***************************************"



