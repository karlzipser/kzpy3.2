#! /usr/bin/python
#//anaconda/bin/python
#
import caffe
caffe.set_device(1)
caffe.set_mode_gpu()
from kzpy3.utils import *
from kzpy3.teg2.data.access.get_data_from_bag_files9 import *
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


def load_data_into_model(solver,data,flip):
	global img
	if data == 'END' :
		print """data = 'END':"""
		return False
	if 'left' in data:
		if type(data['left'][0]) == np.ndarray:
			target_data = list(data['steer'])
			target_data += list(data['motor'])
			target_data[0] = data['steer'][0]
			target_data[10] = data['motor'][0]

			if not flip:
				solver.net.blobs['ZED_data_pool2_left'].data[0,0,:,:] = data['left'][0][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2_left'].data[0,1,:,:] = data['left'][1][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2_left'].data[0,2,:,:] = data['left'][2][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2_right'].data[0,0,:,:] = data['right'][0][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2_right'].data[0,1,:,:] = data['right'][1][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2_right'].data[0,2,:,:] = data['right'][2][:,:]/255.0-.5

			else: # flip left-right
				solver.net.blobs['ZED_data_pool2_left'].data[0,0,:,:] = scipy.fliplr(data['left'][0][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2_left'].data[0,1,:,:] = scipy.fliplr(data['left'][1][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2_left'].data[0,2,:,:] = scipy.fliplr(data['left'][2][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2_right'].data[0,0,:,:] = scipy.fliplr(data['right'][0][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2_right'].data[0,1,:,:] = scipy.fliplr(data['right'][1][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2_right'].data[0,2,:,:] = scipy.fliplr(data['right'][2][:,:]/255.0-.5)

				for i in range(len(target_data)/2):
					t = target_data[i]
					t = t - 49
					t = -t
					t = t + 49
					target_data[i] = t
				if data['meta-turn'] > -10:
					t = data['meta-turn']
					t = t - 49
					t = -t
					t = t + 49					
					data['meta-turn'] = t

			Direct = 0.
			Follow = 0.
			Play = 0.
			Furtive = 0.
			Caf = 0

			#print data['bag_filename']

			if 'follow' in data['path']:
				Follow = 1.0
			if 'direct' in data['path']:
				Direct = 1.0
			if 'play' in data['path']:
				Play = 1.0
			if 'furtive' in data['path']:
				Furtive = 1.0
			if 'caffe' in data['path']:
				Caf = 1.0

			solver.net.blobs['metadata'].data[0,0,:,:] = data['meta-turn']/100.
			solver.net.blobs['metadata'].data[0,1,:,:] = Caf
			solver.net.blobs['metadata'].data[0,2,:,:] = Follow
			solver.net.blobs['metadata'].data[0,3,:,:] = Direct
			solver.net.blobs['metadata'].data[0,4,:,:] = Play
			solver.net.blobs['metadata'].data[0,5,:,:] = Furtive
			#solver.net.blobs['metadata'].data[0,6,:,:] = target_data[0] #current steer
			#solver.net.blobs['metadata'].data[0,7,:,:] = target_data[len(target_data)/2] #current motor
			#solver.net.blobs['metadata'].data[0,8,:,:] = 0
			#solver.net.blobs['metadata'].data[0,9,:,:] = 0


			for i in range(len(target_data)):
				solver.net.blobs['steer_motor_target_data'].data[0,i] = target_data[i]/99.

		else:
			print """not if type(data['left']) == np.ndarray: """+str(time.time())
	else:
		pass #print """not if 'left' in data: """+str(time.time())
		return 'no data'
	#show_solver_data(solver,data,flip,49.,1.)
	return True


def show_solver_data(solver,data,flip,steer_offset,steer_mult):
	caffe_steer_color_color = [1.,0,0]
	human_steer_color_color = [0,0,1.]

	data_img_shape = np.shape(solver.net.blobs['ZED_data_pool2'].data)
	num_frames = (data_img_shape[1])/2
	print num_frames		
	img = np.zeros((data_img_shape[2],data_img_shape[3],3))+0.5
	img[0,0,:]=1
	img[0,1,:]=0
	mi(img)
	plt.pause(0.5)
	for i in range(num_frames):
		#print i
		#if i > 0:
		#    img_prev = img.copy()

		if not flip:
			d = data['left'][i][:,:]/255.0-.5
		else:
			d = scipy.fliplr(data['left'][i][:,:]/255.0-.5)
		d = z2o(d)
		if i < 2:
			img[:,:,0] = z2o(solver.net.blobs['ZED_data_pool2'].data[0,i,:,:])
		else:
			img[:,:,0] = d #z2o(solver.net.blobs['ZED_data_pool2'].data[0,i+2,:,:])
		img[:,:,1] = img[:,:,0].copy()
		img[:,:,2] = img[:,:,0].copy()

		if solver.net.blobs['metadata'].data[0,1,0,0] == 1.0: #caffe is steering
		    steer_rect_color = caffe_steer_color_color
		else:
			steer_rect_color = human_steer_color_color

		steer = 99*solver.net.blobs['steer_motor_target_data'].data[0,0] * steer_mult + steer_offset
		apply_rect_to_img(img,steer,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)

		mi(img,img_title=d2s(flip,i))#,img_title=(d2s('dt = ', int(1000*dt),'ms')))
		#print solver.net.blobs['steer_motor_target_data'].data
		plt.pause(0.25)

bf_dic = {}

def run_solver(solver, bair_car_data, num_steps,flip):
	global img
	global loss
	global bf_dic
	#if time.time() - loss_timer > 60*15:
	#	save_obj(loss,opjD('z2_2nd_pass','loss'))
	step_ctr = 0
	ctr = 0
	if True: #try:
		while step_ctr < num_steps:
			imshow = False
			datashow = False
			if np.mod(ctr,200) == 0:
				imshow = True
			if np.mod(ctr,2010) == 0:
				datashow = True
			"""
			if hasattr(bair_car_data,'bag_folders_weighted'):
				if len(bair_car_data.bag_folders_weighted) == 0:
					print("run_solver:: waiting because len(bair_car_data.bag_folders_weighted) == 0")
					time.sleep(3)
					continue
			else:
				print("run_solver:: waiting because bair_car_data has no bag_folders_weighted")
				time.sleep(3)
				continue
				/home/karlzipser/Desktop/bair_car_data_min/caffe_z2_play_campus_10Oct16_17h58m02s_Mr_Orange
			"""
			while True:
				bf = random.choice(bair_car_data.bag_folders_weighted)
				if '/home/karlzipser/Desktop/bair_car_data_min/follow_caffe_z2_follow_campus_10Oct16_17h27m05s_Mr_Orange' != bf:
					break
				
			#print bf
			if not bf in bf_dic:
				bf_dic[bf] = 0
			bf_dic[bf] += 1
			#print bf,len(bf_dic)
			#time.sleep(0.5)

			BF = bair_car_data.bag_folders_dic[bf]
			meta_turn_flag = False
			rnd = np.random.random()
			if rnd < 7/14.:
				indx,_ = BF.get_random_steer_equal_weighting()
			elif rnd < 13/14.:
				indx,_ = BF.get_random_motor_equal_weighting()
			else:
				indx,_ = get_random_turn_with_high_loss_equal_weighting(BF)
				meta_turn_flag = True
			data = BF.get_data(num_image_steps=3,good_start_index=indx)
			if meta_turn_flag:
				data['meta-turn'] = data['steer'][9]
			else:
				data['meta-turn'] = 49

			result = load_data_into_model(solver, data,flip)
			#result = load_data_into_model(solver, bair_car_data.get_data(['steer','motor'],10,10),flip)
			if result == False:
				break
			if result == True:
				solver.step(1)
				a = solver.net.blobs['steer_motor_target_data'].data[0,:] - solver.net.blobs['ip2'].data[0,:]
				loss.append(np.sqrt(a * a).mean())
				ctr += 1
				if imshow:
					#print (ctr,np.array(loss[-99:]).mean())
					img[:,:,0] = solver.net.blobs['ZED_data_pool2_left'].data[0,0,:,:]
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
					cprint(d2s("\t\tmean loss=",(np.array(loss[-1000:]).mean())),'magenta')
					cprint(solver.net.blobs['metadata'].data[0,:,5,5],'red')
					print array_to_int_list(solver.net.blobs['steer_motor_target_data'].data[0,:][:])
					print array_to_int_list(solver.net.blobs['ip2'].data[0,:][:])
					#time.sleep(2)
			step_ctr += 1
	#except Exception as e:
	#	print "train ***************************************"
	#	print e.message, e.args
	#	print "***************************************"


def array_to_dp_list(a,n=0):
	l = []
	for d in a:
		l.append(dp(d,n))
	return l
def array_to_int_list(a):
	l = []
	for d in a:
		l.append(int(d*100))
	return l

def quit_thread():
	global QUIT
	QUIT = True

def load_bag_folders_thread():
	global DO_LOADING
	global QUIT
	while True:
		if QUIT:
			cprint("load_bag_folders_thread:: QUIT == True",'black','on_green')
			return
		if DO_LOADING == True:
			print("load_bag_folders_thread:: DO_LOADING == True")
			DO_LOADING = False
			bair_car_data.load_bag_folders()
		else:
			time.sleep(1)

def main():
	weights_file_path = most_recent_file_in_folder(opjD('z3'),['z3','caffemodel']) 
	if weights_file_path == "None":
		weights_file_path = None
	if weights_file_path != None:
		print "loading " + weights_file_path
		solver.net.copy_from(weights_file_path)
	filters = load_obj(opjD('filters'))
	for i in range(48):
		solver.net.params['conv1_left'][0].data[i,0,:,:] = z2o(filters[i,1,:,:])-0.5
		solver.net.params['conv1_right'][0].data[i,0,:,:] = z2o(filters[i,1,:,:])-0.5

	while True:
		try:
			load_bag_folders(bair_car_data,num_to_load=2)
			#bair_car_data.load_bag_folders(num_to_load=25)
			pprint(bf_dic)
			for i in range(150):
				if np.random.random() > 0.5:
					flip = False
				else:
					flip = True
				run_solver(solver,bair_car_data,1000,flip)
			t_end()
			#except KeyboardInterrupt:
			#    print 'Interrupted'
		except Exception as e:
			print "train loop ***************************************"
			print e.message, e.args
			print "***************************************"


 



loss_timer = time.time()
loss = []

bair_car_data_path = opjD('bair_car_data_min')#'/media/ExtraDrive1/bair_car_data_min'
assert(len(gg(opj(bair_car_data_path,'*'))) > 5)

list0 = []
list1 = ['play','follow','furtive','caffe','direct_from_campus2_08Oct16_10h15m','direct_from_campus_31Dec12_10h00m','direct_to_campus_08Oct16_08h55m37','Aug','Sep']
list2 = ['Oct','Tilden','play','follow','furtive','play','follow','furtive','caffe','local','Aug','Sep']
list3 = ['follow','furtive','direct_from_campus2_08Oct16_10h15m','direct_from_campus_31Dec12_10h00m','direct_to_campus_08Oct16_08h55m37']

bair_car_data = Bair_Car_Data(bair_car_data_path,list0)
unix('mkdir -p '+opjD('z3'))

solver_file_path = opjh("kzpy3/caf3/z3/solver.prototxt")
#solver_file_path = opjh("kzpy3/caf3/z2_replicate/solver.prototxt")
solver = setup_solver()

#main()
"""
filters = load_obj(opjD('filters'))
for i in range(48):
	solver.net.params['conv1_left'][0].data[i,0,:,:] = z2o(filters[i,1,:,:])-0.5
	solver.net.params['conv1_right'][0].data[i,0,:,:] = z2o(filters[i,1,:,:])-0.5
""";


"""
('steer_motor_target_data', (1, 20))
('ZED_data_pool2_left', (1, 3, 94, 168))
('ZED_data_pool2_right', (1, 3, 94, 168))
('conv1_left', (1, 48, 28, 53))
('conv1_left_1x1a', (1, 48, 28, 53))
('conv1_left_1x1b', (1, 48, 28, 53))
('conv1_right', (1, 48, 28, 53))
('conv1_right_1x1a', (1, 48, 28, 53))
('conv1_right_1x1a_conv1_right_1x1a_relu_0_split_0', (1, 48, 28, 53))
('conv1_right_1x1a_conv1_right_1x1a_relu_0_split_1', (1, 48, 28, 53))
('conv1_right_1x1b', (1, 48, 28, 53))
('conv1_concat', (1, 96, 28, 53))
('conv2', (1, 96, 13, 26))
('metadata', (1, 6, 13, 26))
('conv2_concat', (1, 102, 13, 26))
('conv2_pool', (1, 102, 6, 13))
('conv3', (1, 256, 2, 6))
('conv3_pool', (1, 256, 1, 3))
('ip1', (1, 512))
('ip2', (1, 20))
('euclidean', ())
('conv1_left', (48, 3, 11, 11))
('conv1_left_1x1a', (48, 48, 1, 1))
('conv1_left_1x1b', (48, 48, 1, 1))
('conv1_right', (48, 3, 11, 11))
('conv1_right_1x1a', (48, 48, 1, 1))
('conv1_right_1x1b', (48, 48, 1, 1))
('conv2', (96, 96, 3, 3))
('conv3', (256, 102, 3, 3))
('ip1', (512, 768))
('ip2', (20, 512))
"""