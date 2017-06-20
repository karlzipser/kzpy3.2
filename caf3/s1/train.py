#! /usr/bin/python
#//anaconda/bin/python

import caffe
from kzpy3.utils import *
from kzpy3.teg2.data.access.get_data_from_bag_files5 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt


########################################################
#          SETUP SECTION
#
caf_level = "caf3"
model_name = 's1'
solver_file_path = opjh("kzpy3",caf_level,model_name,"solver.prototxt")
weights_folder = opjD(model_name)
unix("mkdir -p "+weights_folder)
weights_file_path = most_recent_file_in_folder(weights_folder,[model_name,'caffemodel']) 
if weights_file_path == "None":
	weights_file_path = None
#
###### ##################################################
from kzpy3.teg2.data.access.get_data_from_bag_files6 import *
BCD = Bair_Car_Data(opjD('bair_car_data_min'),[])#'caffe','play','follow','Tilden','Aug','Sep'])

#caffe.set_device(1)
caffe.set_mode_cpu()


def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver

solver = setup_solver()
if weights_file_path != None:
	print "loading " + weights_file_path
	solver.net.copy_from(weights_file_path)
loss = []
plt.ion()
for ii in range(100000000):
	if True:#try:
		N=25
		while True:
			bf=an_element(BCD.bag_folders_dic)
			if bf.data['acc_z'].mean() > 5 and len(bf.data['state_one_steps_1s_indicies']) > 1000: # the mean should be around 9.5 if acc is in datafile
				break
		indx = random.choice(bf.data['state_one_steps_1s_indicies'])#[random.randint(0,len(bf.data['state_one_steps_1s_indicies'])-1)]
		topics = ['steer_z_scored','motor_z_scored','acc_x_z_scored','acc_y_z_scored','acc_z_z_scored','gyro_x_z_scored','gyro_y_z_scored','gyro_z_z_scored','encoder_z_scored']
		data = []
		target = []
		target2 = []
		for tp in topics:
			zero_topic = False
			if random.random() < 0.333:
				zero_topic = True
			for i in range(N):
				d = bf.data[tp][indx+i]
				target.append(d)
				if i == N-1:
					target2.append(d)
				if zero_topic:
					d *= 0
				data.append(d)
		#print data
		for i in range(len(data)):
			solver.net.blobs['input_data'].data[0,i] = data[i]

		for i in range(len(target2)):
			solver.net.blobs['target_data'].data[0,i] = target2[i]
		solver.step(1)
		a = solver.net.blobs['target_data'].data[0,:] - solver.net.blobs['ip3'].data[0,:]
		loss.append(np.sqrt(a * a).mean())
		if np.mod(ii,1000) == 0:
			cprint(solver.net.blobs['target_data'].data[0,:],'red')
			cprint(solver.net.blobs['ip3'].data[0,:],'green')
			plt.figure(10)
			plt.clf()
			plt.plot(solver.net.blobs['target_data'].data[0,:],solver.net.blobs['ip3'].data[0,:],'o')
			plt.xlim(-3,3);plt.ylim(-3,3)
			plt.pause(0.01)
			plt.figure(11)
			plt.clf()
			plt.plot(target)
			plt.plot(solver.net.blobs['input_data'].data[0,:])
			plt.pause(0.01)
	#except Exception as e:
	#	print "train loop ***************************************"
	#	print e.message, e.args
	

plt.clf()
plt.plot(loss)









