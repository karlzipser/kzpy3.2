#! /usr/bin/python
#//anaconda/bin/python

import caffe
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files4 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt

USE_GPU = False

########################################################
#          SETUP SECTION
#
solver_file_path1 = opjh("kzpy3/caf3/z2/solver.prototxt")
weights_file_path1 = opjD("z2/z2.caffemodel") #sys.argv[1] #None#opjD('z2_2nd_pass/z2_2nd_pass_iter_30000.caffemodel') #
if weights_file_path1 == "None":
	weights_file_path1 = None
solver_file_path2 = opjh("kzpy3/caf3/z3/solver.prototxt")
weights_file_path2 = None #sys.argv[2] #None#opjD('z2_2nd_pass/z2_2nd_pass_iter_30000.caffemodel') #
if weights_file_path2 == "None":
	weights_file_path2 = None
#
########################################################

def setup_solver(solver_file_path):
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver



img = zeros((94,168,3))#,'uint8')
def load_data_into_model(solver,data,start,num_steps,flip_left_right):
	global img
	if data == 'END' :
		print """data = 'END':"""
		return False
	if 'left' in data:
		if type(data['left'][0]) == np.ndarray:
			target_data = []
			target_data += data['steer'][start:(start+num_steps)]
			target_data += data['motor'][start:(start+num_steps)]

			if flip_left_right: #np.random.random() > 0.5:
				solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = data['left'][0+start][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = data['left'][1+start][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = data['right'][0+start][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = data['right'][1+start][:,:]/255.0-.5

			else: # flip left-right
				solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = scipy.fliplr(data['left'][0+start][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = scipy.fliplr(data['left'][1+start][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = scipy.fliplr(data['right'][0+start][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = scipy.fliplr(data['right'][1+start][:,:]/255.0-.5)
				for i in range(len(target_data)/2):
					t = target_data[i]
					t = t - 49
					t = -t
					t = t + 49
					target_data[i] = t

			Direct = 0.
			Follow = 0.
			Play = 0.
			Furtive = 0.
			Caf = 0

			if 'follow' in data['bag_filename']:
				Follow = 1.0
			if 'direct' in data['bag_filename']:
				Direct = 1.0
			if 'play' in data['bag_filename']:
				Play = 1.0
			if 'furtive' in data['bag_filename']:
				Furtive = 1.0
			if 'caffe' in data['bag_filename']:
				Caf = 1.0

			solver.net.blobs['metadata'].data[0,0,:,:] = 0#target_data[0]/99. #current steer
			solver.net.blobs['metadata'].data[0,1,:,:] = Caf #0#target_data[len(target_data)/2]/99. #current motor
			solver.net.blobs['metadata'].data[0,2,:,:] = Follow
			solver.net.blobs['metadata'].data[0,3,:,:] = Direct
			solver.net.blobs['metadata'].data[0,4,:,:] = Play
			solver.net.blobs['metadata'].data[0,5,:,:] = Furtive
			
			for i in range(len(target_data)):
				solver.net.blobs['steer_motor_target_data'].data[0,i] = target_data[i]/99.

		else:
			print """not if type(data['left']) == np.ndarray: """+str(time.time())
	else:
		pass #print """not if 'left' in data: """+str(time.time())
		return 'no data'
	return True


loss_timer = time.time()
loss = []
def run_solver(solver, bair_car_data, num_steps):
	global img
	global loss

	step_ctr = 0
	ctr = 0
	if True:
		while step_ctr < num_steps:
			imshow = False
			datashow = False
			if np.mod(ctr,50) == 0:
				imshow = True
			if np.mod(ctr,1000) == 0:
				datashow = True
			result = load_data_into_model(solver, bair_car_data.get_data(['steer','motor'],10,2))
			if result == False:
				break
			if result == True:
				solver.step(1)
				a = solver.net.blobs['steer_motor_target_data'].data[0,:] - solver.net.blobs['ip2'].data[0,:]
				loss.append(np.sqrt(a * a).mean())
				ctr += 1
				if imshow:
					img[:,:,0] = solver.net.blobs['ZED_data_pool2'].data[0,0,:,:]
					img += 0.5
					img *= 255.
					img[:,:,1] = img[:,:,0]
					img[:,:,2] = img[:,:,0]
					cv2.imshow('left',img.astype('uint8'))

					if cv2.waitKey(1) & 0xFF == ord('q'):
					    pass
			
				if datashow:
					print (ctr,np.array(loss[-99:]).mean())
					print(solver.net.blobs['metadata'].data[0,:,5,5])
					print array_to_int_list(solver.net.blobs['steer_motor_target_data'].data[0,:][:])
					print array_to_int_list(solver.net.blobs['ip2'].data[0,:][:])
			step_ctr += 1


def array_to_int_list(a):
	l = []
	for d in a:
		l.append(int(d*100))
	return l



#if __name__ == '__main__':

unix('mkdir -p '+opjD('z3'))



if USE_GPU:
	caffe.set_device(0)
	caffe.set_mode_gpu()

solver1_list = []
for i in range(2):
	solver1_list.append(setup_solver(solver_file_path1))
	if weights_file_path1 != None:
		print "loading " + weights_file_path1
		solver1_list[i].net.copy_from(weights_file_path1)


solver2 = setup_solver(solver_file_path2)
if weights_file_path2 != None:
	print "loading " + weights_file_path2
	solver2.net.copy_from(weights_file_path2)

#bair_car_data = Bair_Car_Data(opjD('temp'),1000,100)
#bair_car_data = Bair_Car_Data(opjD('temp_bags_saved/folder'),1000,100)
bair_car_data = Bair_Car_Data(opjD('bair_car_data_min'),1000,100)

ctr = 0
loss = []
img = zeros((94,168,3))

while True:

	data = bair_car_data.get_data(['steer','motor'],32,32)
	flip_left_right = False
	if np.random.random() < 0.5:
		flip_left_right = True
	load_data_into_model(solver1_list[0],data,0,10,flip_left_right)
	solver1_list[0].net.forward(end='conv2')
	load_data_into_model(solver1_list[1],data,2,10,flip_left_right)
	solver1_list[1].net.forward(end='conv2')

	solver2.net.blobs['conv2_PAST'].data[:] = solver1_list[0].net.blobs['conv2'].data[:]
	solver2.net.blobs['conv2_PRESENT'].data[:] = solver1_list[1].net.blobs['conv2'].data[:]
	solver2.net.blobs['steer_motor_target_data'].data[:] = solver1_list[1].net.blobs['steer_motor_target_data'].data[:]
	solver2.step(1)

	a = solver2.net.blobs['steer_motor_target_data'].data[0,:] - solver2.net.blobs['ip2'].data[0,:]
	loss.append(np.sqrt(a * a).mean())
	imshow = False
	datashow = False
	if np.mod(ctr,10) == 0:
		imshow = True
	if np.mod(ctr,50) == 0:
		datashow = True
	if datashow:
		if len(loss) > 1000:
			print (ctr,np.array(loss[-1000:]).mean())
		print array_to_int_list(solver2.net.blobs['steer_motor_target_data'].data[0,:][:])
		print array_to_int_list(solver2.net.blobs['ip2'].data[0,:][:])

	if imshow:
		img[:,:,0] = solver1_list[1].net.blobs['ZED_data_pool2'].data[0,0,:,:]
		img += 0.5
		img *= 255.
		img[:,:,1] = img[:,:,0]
		img[:,:,2] = img[:,:,0]
		cv2.imshow('left',img.astype('uint8'))
		if cv2.waitKey(1) & 0xFF == ord('q'):
		    pass

	ctr += 1

