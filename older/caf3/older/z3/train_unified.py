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
weights_file_path2 = opjD('z3/z3_iter_705000.caffemodel')
if weights_file_path2 == "None":
	weights_file_path2 = None

solver_file_path3 = opjh("kzpy3/caf3/z3/solver_4.prototxt")
weights_file_path3 = opjD('z3/z3_4_iter_130000.caffemodel')
if weights_file_path3 == "None":
	weights_file_path3 = None

solver_file_path4 = opjh("kzpy3/caf3/z3/solver_5.prototxt")
weights_file_path4 = opjD('z3/z3_5_iter_200000.caffemodel')
if weights_file_path4 == "None":
	weights_file_path4 = None

solver_file_path5 = opjh("kzpy3/caf3/z3/solver_6.prototxt")
weights_file_path5 = opjD('z3/z3_6_iter_70000.caffemodel')
if weights_file_path5 == "None":
	weights_file_path5 = None

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
				solver.net.blobs['ZED_data_pool2__'+str(start)].data[0,0,:,:] = data['left'][0+2*start][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2__'+str(start)].data[0,1,:,:] = data['left'][1+2*start][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2__'+str(start)].data[0,2,:,:] = data['right'][0+2*start][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2__'+str(start)].data[0,3,:,:] = data['right'][1+2*start][:,:]/255.0-.5

			else: # flip left-right
				solver.net.blobs['ZED_data_pool2__'+str(start)].data[0,0,:,:] = scipy.fliplr(data['left'][0+2*start][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2__'+str(start)].data[0,1,:,:] = scipy.fliplr(data['left'][1+2*start][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2__'+str(start)].data[0,2,:,:] = scipy.fliplr(data['right'][0+2*start][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2__'+str(start)].data[0,3,:,:] = scipy.fliplr(data['right'][1+2*start][:,:]/255.0-.5)
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

			solver.net.blobs['metadata__'+str(start)].data[0,0,:,:] = 0#target_data[0]/99. #current steer
			solver.net.blobs['metadata__'+str(start)].data[0,1,:,:] = Caf #0#target_data[len(target_data)/2]/99. #current motor
			solver.net.blobs['metadata__'+str(start)].data[0,2,:,:] = Follow
			solver.net.blobs['metadata__'+str(start)].data[0,3,:,:] = Direct
			solver.net.blobs['metadata__'+str(start)].data[0,4,:,:] = Play
			solver.net.blobs['metadata__'+str(start)].data[0,5,:,:] = Furtive
			
			for i in range(len(target_data)):
				solver.net.blobs['steer_motor_target_data__'+str(7)].data[0,i] = target_data[i]/99.

		else:
			print """not if type(data['left']) == np.ndarray: """+str(time.time())
	else:
		pass #print """not if 'left' in data: """+str(time.time())
		return 'no data'
	return True


loss_timer = time.time()
loss = []


def array_to_int_list(a):
	l = []
	for d in a:
		l.append(int(d*100))
	return l



#if __name__ == '__main__':

#unix('mkdir -p '+opjD('z3'))



if USE_GPU:
	caffe.set_device(0)
	caffe.set_mode_gpu()

"""
solver1 = setup_solver(solver_file_path1)
solver2 = setup_solver(solver_file_path2)
solver3 = setup_solver(solver_file_path3)
solver4 = setup_solver(solver_file_path4)
solver5 = setup_solver(solver_file_path5)
"""

solver_unified = setup_solver(opjh('kzpy3/caf3/z3/solver_unified.prototxt'))
solver_unified.net.copy_from(opjD('z3/z_unified_iter_90000.caffemodel'))

"""
for h in range(8):
	for i in range(2):
		solver_unified.net.params['conv1__'+str(h)][i].data[:] = solver1.net.params['conv1'][i].data[:].copy()

for h in range(8):
	for i in range(2):
		solver_unified.net.params['conv2__'+str(h)][i].data[:] = solver1.net.params['conv2'][i].data[:].copy()

for h in range(4):
	for i in range(2):
		solver_unified.net.params['conv2_2__'+str(h)][i].data[:] = solver2.net.params['conv2_2'][i].data[:].copy()
		solver_unified.net.params['conv3_2__'+str(h)][i].data[:] = solver2.net.params['conv3_2'][i].data[:].copy()

for h in range(2):
	for i in range(2):
		solver_unified.net.params['conv3_2_2__'+str(h)][i].data[:] = solver3.net.params['conv3_2_2'][i].data[:].copy()
		solver_unified.net.params['conv4_2__'+str(h)][i].data[:] = solver3.net.params['conv4_2'][i].data[:].copy()

for h in range(1):
	for i in range(2):
		solver_unified.net.params['conv4_2_2__'+str(h)][i].data[:] = solver4.net.params['conv4_2_2'][i].data[:].copy()
		solver_unified.net.params['conv5_2__'+str(h)][i].data[:] = solver4.net.params['conv5_2'][i].data[:].copy()

for h in range(2,3):
	for i in range(2):
		print 'ip1_conv'+str(h)+'_2'
		solver_unified.net.params['ip1_conv'+str(h)+'_2'][i].data[:] = solver1.net.params['ip1'][i].data[:].copy()
		solver_unified.net.params['ip1_conv'+str(h)+'_2'][i].data[:] = solver1.net.params['ip1'][i].data[:].copy()
for h in range(3,4):
	for i in range(2):
		print 'ip1_conv'+str(h)+'_2'
		solver_unified.net.params['ip1_conv'+str(h)+'_2'][i].data[:] = solver2.net.params['ip1'][i].data[:].copy()
		solver_unified.net.params['ip1_conv'+str(h)+'_2'][i].data[:] = solver2.net.params['ip1'][i].data[:].copy()

for h in range(4,5):
	for i in range(2):
		print 'ip1_conv'+str(h)+'_2'
		solver_unified.net.params['ip1_conv'+str(h)+'_2'][i].data[:] = solver3.net.params['ip1'][i].data[:].copy()
		solver_unified.net.params['ip1_conv'+str(h)+'_2'][i].data[:] = solver3.net.params['ip1'][i].data[:].copy()

for h in range(5,6):
	for i in range(2):
		print 'ip1_conv'+str(h)+'_2'
		solver_unified.net.params['ip1_conv'+str(h)+'_2'][i].data[:] = solver4.net.params['ip1'][i].data[:].copy()
		solver_unified.net.params['ip1_conv'+str(h)+'_2'][i].data[:] = solver4.net.params['ip1'][i].data[:].copy()
"""

"""
('ip1_conv2_2', (1, 512))
('ip1_conv3_2', (1, 512))
('ip1_conv4_2', (1, 512))
('ip1_conv5_2', (1, 512))
('ip1_concat', (1, 2048))
('ip1_2', (1, 96))
('ip2', (1, 20))
"""


bair_car_data = Bair_Car_Data(opjD('bair_car_data_min'),1,10)
#bair_car_data = Bair_Car_Data(opjD('temp'),1000,100)

ctr = 0
loss = []
img = zeros((94,168,3))

while True:

	data = bair_car_data.get_data(['steer','motor'],32+16,16)
	flip_left_right = False
	if np.random.random() < 0.5:
		flip_left_right = True
	for i in range(0,8):
		load_data_into_model(solver_unified,data,i,32,flip_left_right)

	solver_unified.step(1)

	a = solver_unified.net.blobs['steer_motor_target_data__7'].data[0,:] - solver_unified.net.blobs['ip2'].data[0,:]

	loss.append(np.sqrt(a * a).mean())

	imshow = False
	datashow = False
	do_avg = False
	if np.mod(ctr,1) == 0:
		imshow = True
	if np.mod(ctr,5) == 0:
		datashow = True
	if np.mod(ctr,10) == 0:
		do_avg = True

	if datashow:		
		if len(loss) > 1000:
			print (ctr,np.array(loss[-1000:]).mean())
		print array_to_int_list(solver_unified.net.blobs['steer_motor_target_data__7'].data[0,:][:])
		print array_to_int_list(solver_unified.net.blobs['ip2'].data[0,:][:])

	if do_avg:
		for i in range(2):
			temp = solver_unified.net.params['conv1__0'][i].data[:]
			for h in range(1,8):
				temp += solver_unified.net.params['conv1__'+str(h)][i].data[:]
			temp /= 8.
			for h in range(8):
				solver_unified.net.params['conv1__'+str(h)][i].data[:] = temp.copy()

			temp = solver_unified.net.params['conv2__0'][i].data[:]
			for h in range(1,8):
				temp += solver_unified.net.params['conv2__'+str(h)][i].data[:]
			temp /= 8.
			for h in range(8):
				solver_unified.net.params['conv2__'+str(h)][i].data[:] = temp.copy()

		for i in range(2):
			temp = solver_unified.net.params['conv2_2__0'][i].data[:]
			for h in range(1,4):
				temp += solver_unified.net.params['conv2_2__'+str(h)][i].data[:]
			temp /= 4.
			for h in range(4):
				solver_unified.net.params['conv2_2__'+str(h)][i].data[:] = temp.copy()

			temp = solver_unified.net.params['conv3_2__0'][i].data[:]
			for h in range(1,4):
				temp += solver_unified.net.params['conv3_2__'+str(h)][i].data[:]
			temp /= 4.
			for h in range(4):
				solver_unified.net.params['conv3_2__'+str(h)][i].data[:] = temp.copy()


		for i in range(2):
			temp = solver_unified.net.params['conv3_2_2__0'][i].data[:]
			for h in range(1,2):
				temp += solver_unified.net.params['conv3_2_2__'+str(h)][i].data[:]
			temp /= 2.
			for h in range(2):
				solver_unified.net.params['conv3_2_2__'+str(h)][i].data[:] = temp.copy()

			temp = solver_unified.net.params['conv4_2__0'][i].data[:]
			for h in range(1,2):
				temp += solver_unified.net.params['conv4_2__'+str(h)][i].data[:]
			temp /= 2.
			for h in range(2):
				solver_unified.net.params['conv4_2__'+str(h)][i].data[:] = temp.copy()

		for i in range(2):
			temp = solver_unified.net.params['conv4_2_2__0'][i].data[:]
			for h in range(1,1):
				temp += solver_unified.net.params['conv4_2_2__'+str(h)][i].data[:]
			temp /= 1.
			for h in range(1):
				solver_unified.net.params['conv4_2_2__'+str(h)][i].data[:] = temp.copy()

			temp = solver_unified.net.params['conv5_2__0'][i].data[:]
			for h in range(1,1):
				temp += solver_unified.net.params['conv5_2__'+str(h)][i].data[:]
			temp /= 1.
			for h in range(1):
				solver_unified.net.params['conv5_2__'+str(h)][i].data[:] = temp.copy()






	if imshow:
		img[:,:,0] = solver_unified.net.blobs['ZED_data_pool2__7'].data[0,0,:,:]
		img += 0.5
		img *= 255.
		img[:,:,1] = img[:,:,0]
		img[:,:,2] = img[:,:,0]
		cv2.imshow('left',img.astype('uint8'))
		if cv2.waitKey(1) & 0xFF == ord('q'):
		    pass

	ctr += 1

	if False:
		for i in range(8):
			for j in range(2):
				mi(solver_unified.net.blobs['ZED_data_pool2__'+str(i)].data[0,j,:,:])
				plt.pause(0.5)