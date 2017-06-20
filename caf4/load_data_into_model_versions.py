from kzpy3.vis import *

import cv2
blue = [0,0,0.8]
blue_green = [0,0.5,0.5]

def load_data_into_model_version_1(solver,data,flip,show_data=False):
	if 'left' in data:
		if len(data['left']) >= 10:

			if type(data['left'][0]) == np.ndarray:
				target_data = data['steer'][:10]
				target_data += data['motor'][:10]

				if not flip:
					solver.net.blobs['ZED_data'].data[0,0,:,:] = data['left'][0][:,:,0]
					solver.net.blobs['ZED_data'].data[0,1,:,:] = data['left'][1][:,:,0]
					solver.net.blobs['ZED_data'].data[0,2,:,:] = data['right'][0][:,:,0]
					solver.net.blobs['ZED_data'].data[0,3,:,:] = data['right'][1][:,:,0]
					solver.net.blobs['ZED_data'].data[0,4,:,:] = data['left'][0][:,:,1]
					solver.net.blobs['ZED_data'].data[0,5,:,:] = data['left'][1][:,:,1]
					solver.net.blobs['ZED_data'].data[0,6,:,:] = data['right'][0][:,:,1]
					solver.net.blobs['ZED_data'].data[0,7,:,:] = data['right'][1][:,:,1]
					solver.net.blobs['ZED_data'].data[0,8,:,:] = data['left'][0][:,:,2]
					solver.net.blobs['ZED_data'].data[0,9,:,:] = data['left'][1][:,:,2]
					solver.net.blobs['ZED_data'].data[0,10,:,:] = data['right'][0][:,:,2]
					solver.net.blobs['ZED_data'].data[0,11,:,:] = data['right'][1][:,:,2]
					

				else: # flip left-right
					solver.net.blobs['ZED_data'].data[0,0,:,:] = data['left_flip'][0][:,:,0]
					solver.net.blobs['ZED_data'].data[0,1,:,:] = data['left_flip'][1][:,:,0]
					solver.net.blobs['ZED_data'].data[0,2,:,:] = data['right_flip'][0][:,:,0]
					solver.net.blobs['ZED_data'].data[0,3,:,:] = data['right_flip'][1][:,:,0]
					solver.net.blobs['ZED_data'].data[0,4,:,:] = data['left_flip'][0][:,:,1]
					solver.net.blobs['ZED_data'].data[0,5,:,:] = data['left_flip'][1][:,:,1]
					solver.net.blobs['ZED_data'].data[0,6,:,:] = data['right_flip'][0][:,:,1]
					solver.net.blobs['ZED_data'].data[0,7,:,:] = data['right_flip'][1][:,:,1]
					solver.net.blobs['ZED_data'].data[0,8,:,:] = data['left_flip'][0][:,:,2]
					solver.net.blobs['ZED_data'].data[0,9,:,:] = data['left_flip'][1][:,:,2]
					solver.net.blobs['ZED_data'].data[0,10,:,:] = data['right_flip'][0][:,:,2]
					solver.net.blobs['ZED_data'].data[0,11,:,:] = data['right_flip'][1][:,:,2]

					"""
						solver.net.blobs['ZED_data'].data[0,0,:,:] = data['left_flip'][0][:,:,0]#/255.0-.5
						solver.net.blobs['ZED_data'].data[0,1,:,:] = data['left_flip'][1][:,:,0]#/255.0-.5
						solver.net.blobs['ZED_data'].data[0,2,:,:] = data['right_flip'][0][:,:,0]#/255.0-.5
						solver.net.blobs['ZED_data'].data[0,3,:,:] = data['right_flip'][1][:,:,0]#/255.0-.5
						solver.net.blobs['ZED_data'].data[0,4,:,:] = data['left_flip'][0][:,:,1]#/255.0-.5
						solver.net.blobs['ZED_data'].data[0,5,:,:] = data['left_flip'][1][:,:,1]#/255.0-.5
						solver.net.blobs['ZED_data'].data[0,6,:,:] = data['right_flip'][0][:,:,1]#/255.0-.5
						solver.net.blobs['ZED_data'].data[0,7,:,:] = data['right_flip'][1][:,:,1]#/255.0-.5
						solver.net.blobs['ZED_data'].data[0,8,:,:] = data['left_flip'][0][:,:,2]#/255.0-.5
						solver.net.blobs['ZED_data'].data[0,9,:,:] = data['left_flip'][1][:,:,2]#/255.0-.5
						solver.net.blobs['ZED_data'].data[0,10,:,:] = data['right_flip'][0][:,:,2]#/255.0-.5
						solver.net.blobs['ZED_data'].data[0,11,:,:] = data['right_flip'][1][:,:,2]#/255.0-.5

					"""

					"""
					solver.net.blobs['ZED_data'].data[0,0,:,:] = scipy.fliplr(data['left'][0][:,:,0])
					solver.net.blobs['ZED_data'].data[0,1,:,:] = scipy.fliplr(data['left'][1][:,:,0])
					solver.net.blobs['ZED_data'].data[0,2,:,:] = scipy.fliplr(data['right'][0][:,:,0])
					solver.net.blobs['ZED_data'].data[0,3,:,:] = scipy.fliplr(data['right'][1][:,:,0])
					solver.net.blobs['ZED_data'].data[0,4,:,:] = scipy.fliplr(data['left'][0][:,:,1])
					solver.net.blobs['ZED_data'].data[0,5,:,:] = scipy.fliplr(data['left'][1][:,:,1])
					solver.net.blobs['ZED_data'].data[0,6,:,:] = scipy.fliplr(data['right'][0][:,:,1])
					solver.net.blobs['ZED_data'].data[0,7,:,:] = scipy.fliplr(data['right'][1][:,:,1])					
					solver.net.blobs['ZED_data'].data[0,8,:,:] = scipy.fliplr(data['left'][0][:,:,2])
					solver.net.blobs['ZED_data'].data[0,9,:,:] = scipy.fliplr(data['left'][1][:,:,2])
					solver.net.blobs['ZED_data'].data[0,10,:,:] = scipy.fliplr(data['right'][0][:,:,2])
					solver.net.blobs['ZED_data'].data[0,11,:,:] = scipy.fliplr(data['right'][1][:,:,2])
					"""

					for i in range(len(target_data)/2):
						t = target_data[i]
						t = t - 49
						t = -t
						t = t + 49
						target_data[i] = t

				solver.net.blobs['ZED_data'].data[:,:,:,:] -= 128

				Direct = 0.
				Follow = 0.
				Play = 0.
				Furtive = 0.
				Caf = 0

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

				solver.net.blobs['metadata'].data[0,0,:,:] = 0#target_data[0]/99. #current steer
				solver.net.blobs['metadata'].data[0,1,:,:] = Caf#target_data[len(target_data)/2]/99. #current motor
				solver.net.blobs['metadata'].data[0,2,:,:] = Follow
				solver.net.blobs['metadata'].data[0,3,:,:] = Direct
				solver.net.blobs['metadata'].data[0,4,:,:] = Play
				solver.net.blobs['metadata'].data[0,5,:,:] = Furtive

				for i in range(len(target_data)):
					solver.net.blobs['steer_motor_target_data'].data[0,i] = target_data[i]/99.
			if show_data:
				for i in range(len(data['left'])):
					img = data['left'][i].copy()
					steer = data['steer'][i]
					motor = data['motor'][i]
					gyro_x = data['gyro_x'][i]
					gyro_yz_mag = data['gyro_yz_mag'][i]

					apply_rect_to_img(img,steer,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)
					apply_rect_to_img(img,motor,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=False)
					apply_rect_to_img(img,gyro_yz_mag,-150,150,steer_rect_color,steer_rect_color,0.13,0.03,center=True,reverse=True,horizontal=False)
					apply_rect_to_img(img,gyro_x,-150,150,steer_rect_color,steer_rect_color,0.16,0.03,center=True,reverse=True,horizontal=False)

					cv2.imshow('left',cv2.cvtColor(img,cv2.COLOR_RGB2BGR))#.astype('uint8')
					if cv2.waitKey(33) & 0xFF == ord('q'):
					    break
		return True

	return False

def visualize_solver_data_version_1(solver,flip):
	layer_to_use = 'ZED_data_pool2'
	for i in range(2):
		#data_img_shape = np.shape(solver.net.blobs['ZED_data'].data)
		data_img_shape = np.shape(solver.net.blobs[layer_to_use].data)
		img = np.zeros((data_img_shape[2],data_img_shape[3],3))

		#img[:,:,0] = z2o(solver.net.blobs['ZED_data'].data[0,i,:,:])
		#img[:,:,1] = img[:,:,0].copy()
		#img[:,:,2] = img[:,:,0].copy()

		#img[:,:,0] = z2o(solver.net.blobs['ZED_data'].data[0,i,:,:])
		#img[:,:,1] = z2o(solver.net.blobs['ZED_data'].data[0,i+4,:,:])
		#img[:,:,2] = z2o(solver.net.blobs['ZED_data'].data[0,i+8,:,:])

		img[:,:,0] = solver.net.blobs[layer_to_use].data[0,i,:,:]
		img[:,:,1] = solver.net.blobs[layer_to_use].data[0,i+4,:,:]
		img[:,:,2] = solver.net.blobs[layer_to_use].data[0,i+8,:,:]

		img = z2o(img)

		steer = solver.net.blobs['steer_motor_target_data'].data[0,i]*99.
		motor = solver.net.blobs['steer_motor_target_data'].data[0,i+10]*99.

		if flip:
			steer_rect_color = blue_green
		else:
			steer_rect_color = blue
		#print(img.min(),img.max())
		apply_rect_to_img(img,steer,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)
		apply_rect_to_img(img,motor,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=False)
		mi(img)

		pause(0.001)
		#cv2.imshow('left',cv2.cvtColor((255*img).astype(np.uint8),cv2.COLOR_RGB2BGR))#.astype('uint8')
		#if cv2.waitKey(33) & 0xFF == ord('q'):
		#    break
	return True



def load_data_into_model_version_2(solver,data,flip):
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

				solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = data['left'][0][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = data['left'][1][:,:]/255.0-.5
				#solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = data['left'][2][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = data['right'][0][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = data['right'][1][:,:]/255.0-.5
				#solver.net.blobs['ZED_data_pool2'].data[0,5,:,:] = data['right'][2][:,:]/255.0-.5

			else: # flip left-right
				solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = scipy.fliplr(data['left'][0][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = scipy.fliplr(data['left'][1][:,:]/255.0-.5)
				#solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = scipy.fliplr(data['left'][2][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = scipy.fliplr(data['right'][0][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = scipy.fliplr(data['right'][1][:,:]/255.0-.5)
				#solver.net.blobs['ZED_data_pool2'].data[0,5,:,:] = scipy.fliplr(data['right'][2][:,:]/255.0-.5)
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

