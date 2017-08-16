#! /usr/bin/python
#//anaconda/bin/python

import caffe
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files3 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt


########################################################
#          SETUP SECTION
#
solver_file_path = opjh("kzpy3/caf3/z2_3rd_pass/solver.prototxt")
#weights_file_path = None #opjD('z2/z2.caffemodel') #
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

			if np.random.random() > 0.5:
				solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = data['left'][0][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = data['left'][1][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = data['right'][0][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = data['right'][1][:,:]/255.0-.5

			else: # flip left-right
				solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = scipy.fliplr(data['left'][0][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = scipy.fliplr(data['left'][1][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = scipy.fliplr(data['right'][0][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = scipy.fliplr(data['right'][1][:,:]/255.0-.5)
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

			#print data['bag_filename']

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


			#print solver.net.blobs['metadata'].data[0,:,5,5]
			#time.sleep(0.01)


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
	global img
	global loss
	#if time.time() - loss_timer > 60*15:
	#	save_obj(loss,opjD('z2','loss'))

	step_ctr = 0
	ctr = 0
	if True: #try:
		while step_ctr < num_steps:
			imshow = False
			datashow = False
			if np.mod(ctr,50) == 0:
				imshow = True
			if np.mod(ctr,1001) == 0:
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
					#print (ctr,np.array(loss[-99:]).mean())
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
					#print np.round(solver.net.blobs['steer_motor_target_data'].data[0,:][:3],3)
					#print np.round(solver.net.blobs['ip2'].data[0,:][:3],3)
			

				if datashow:
					print (ctr,np.array(loss[-1000:]).mean())
					print(solver.net.blobs['metadata'].data[0,:,5,5])
					print array_to_int_list(solver.net.blobs['steer_motor_target_data'].data[0,:][:])
					print array_to_int_list(solver.net.blobs['ip2'].data[0,:][:])
			step_ctr += 1
	#except Exception as e:
	#	print "train ***************************************"
	#	print e.message, e.args
	#	print "***************************************"


def array_to_int_list(a):
	l = []
	for d in a:
		l.append(int(d*100))
	return l


caffe.set_device(0)
caffe.set_mode_gpu()
#if __name__ == '__main__':

unix('mkdir -p '+opjD('z2_3nd_pass'))
#bair_car_data = Bair_Car_Data('/home/karlzipser/Desktop/bair_car_data/',1000,100)
bair_car_data = Bair_Car_Data('/home/karlzipser/Desktop/bair_car_data_min/',1000,100)
#BF=             Bair_Car_Data('/home/karlzipser/Desktop/z1/bair_car_data/',10,2) 

solver = setup_solver()

weights_file_path = most_recent_file_in_folder(opjD('z2_3rd_pass'),['z2_3rd_pass','caffemodel']) 
if weights_file_path == "None":
	weights_file_path = None
if weights_file_path != None:
	print "loading " + weights_file_path
	solver.net.copy_from(weights_file_path)


def main():
	while True:
		try:
			run_solver(solver,bair_car_data,3000)
		except Exception as e:
			print "train loop ***************************************"
			print e.message, e.args
			print "***************************************"



