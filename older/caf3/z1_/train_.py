#! /usr/bin/python 
#//anaconda/bin/python

import caffe
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files import *

os.chdir(home_path) # this is for the sake of the train_val.prototxt


########################################################
#          SETUP SECTION
#
solver_file_path = opjh("kzpy3/caf3/z1/solver.prototxt")
weights_file_path = opjD('z1/z1_iter_12000.caffemodel') #None #
#
########################################################




def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver


bag_folder_path = '/media/ubuntu/bair_car_data_3/bair_car_data/direct_7Sept2016_Mr_Orange_Tilden'

d = Bair_Car_Recorded_Data(bag_folder_path,10,['steer','motor','encoder','acc','gyro'],2)

def load_data_into_model(solver,data,imshow=False):
	if data == 'END' :
		print """data = 'END':"""
		return False
	if 'left' in data:
		if type(data['left'][0]) == np.ndarray:
			target_data = data['steer']
			target_data += data['motor']

			if imshow:
				cv2.imshow('left',data['left'][0])
				cv2.imshow('right',data['right'][0])
				if cv2.waitKey(1) & 0xFF == ord('q'):
				    pass

			solver.net.blobs['ZED_data'].data[0,0,:,:] = data['left'][0][:,:,1]
			solver.net.blobs['ZED_data'].data[0,1,:,:] = data['left'][1][:,:,1]
			solver.net.blobs['ZED_data'].data[0,2,:,:] = data['right'][0][:,:,1]
			solver.net.blobs['ZED_data'].data[0,3,:,:] = data['right'][1][:,:,1]

			for i in range(len(target_data)):
				solver.net.blobs['steer_motor_target_data'].data[0,i] = target_data[i]

		else:
			print """not if type(data['left']) == np.ndarray: """+str(time.time())
	else:
		pass #print """not if 'left' in data: """+str(time.time())
		return 'no data'
	return True

# 
#
loss = []
def run_solver(solver,d):
	global loss
	ctr = 0
	while True:
		imshow = False
		if np.mod(ctr,10) == 0:
			imshow = True
		result = load_data_into_model(solver,d.get_data('bgr8'),imshow)
		if result == False:
			break
		if result == True:
			solver.step(1)
			a = solver.net.blobs['steer_motor_target_data'].data[0,:] - solver.net.blobs['ip2'].data[0,:]
			loss.append(np.sqrt(a * a).mean())
			ctr += 1
			if np.mod(ctr,10) == 0:
				print (ctr,loss[-1])
			"""
			if np.mod(ctr,100) == 0:
				plt.figure('loss')
				plt.clf()
				plt.plot(loss)
				plt.show()
			"""

if __name__ == '__main__':
	caffe.set_device(0)
	caffe.set_mode_gpu()
	solver = setup_solver()
	
	if weights_file_path != None:
		print "loading " + weights_file_path
		solver.net.copy_from(weights_file_path)
	run_solver(solver,d)




