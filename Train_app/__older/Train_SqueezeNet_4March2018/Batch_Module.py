from Parameters_Module import *
exec(identify_file_str)
from kzpy3.vis2 import *
import torch
import torch.nn.utils as nnutils
import Activity_Module


_ = dictionary_access


#control_filter1 = zeros(90); control_filter1[:5] = 1.0; control_filter1[5:10] = 0.5
#control_filter2 = 1.0/((arange(90)/60.0)**2+1.0); control_filter2[:5] = 0.0; control_filter2[5:10] = 0.5

img_juggled = 0
Loaded_image_files = P['Loaded_image_files']
#data_moments_indexed = P['data_moments_indexed']
data_moments_indexed_loaded = []

DIRECT = 'Direct_Arena_Potential_Field'
FOLLOW = 'Follow_Arena_Potential_Field'
CLOCKWISE = 0
COUNTER_C = 1
long_ctr = -1
P['LOSS_LIST'] = []
P['LOSS_LIST_AVG'] = []

loss_timer = P['loss_timer']

reload_image_file_timer = P['reload_image_file_timer']
reload_image_file_timer.trigger()
frequency_timer = Timer(10.0)

DIRECT = 'Direct_Arena_Potential_Field'
FOLLOW = 'Follow_Arena_Potential_Field'
CLOCKWISE = 0
COUNTER_C = 1

def Batch(the_network=None):
	D = {}
	D['network'] = the_network
	True
	D['batch_size'] = P[BATCH_SIZE]
	D['camera_data'] = torch.FloatTensor().cuda()
	D['metadata'] = torch.FloatTensor().cuda()
	D['target_data'] = torch.FloatTensor().cuda()
	D['names'] = []
	D['states'] = []

	def _load_image_files():
		global data_moments_indexed_loaded
		spd2s('_load_image_files()')
		Loaded_image_files = {}

		shuffled_keys = P['run_name_to_run_path'].keys()
		random.shuffle(shuffled_keys)

		for f in shuffled_keys[:300]:# P['run_name_to_run_path'].keys():#shuffled_keys[:3]:#P['run_name_to_run_path'].keys():
			#spd2s(f)
			Loaded_image_files[f] = {}
			if True:
				try:
					O = h5r(opj(P['run_name_to_run_path'][f],'original_timestamp_data.h5py'))
					F = h5r(opj(P['run_name_to_run_path'][f],'flip_images.h5py'))
					Loaded_image_files[f]['normal'] = O
					Loaded_image_files[f]['flip'] = F
					#print f
				except Exception as e:
					print("********** Exception ***********************")
					print(e.message, e.args)

		"""
		Be able to specify the mix of moments (e.g., 1.0  of normal, 0.1 of heading_pause, 0.5 of LCR, etc...)
		"""


		P['Loaded_image_files'] = Loaded_image_files

		data_moments = []
		data_moments += P['data_moments_indexed']
		pd2s('1) len(data_moments) =',len(data_moments))
		indicies = range(len(P['heading_pause_data_moments_indexed']))
		random.shuffle(indicies)
		num_heading_pause = int(min(0.1*len(data_moments),len(indicies)))
		for i in range(num_heading_pause):
			data_moments.append(P['heading_pause_data_moments_indexed'][indicies[i]])
		pd2s('2) len(data_moments) =',len(data_moments))

		timer = Timer()
		data_moments_indexed_loaded = []
		for dm in data_moments:
			if dm['run_name'] in P['Loaded_image_files']:
				#if dm['other_car_in_view'] == True:
				data_moments_indexed_loaded.append(dm)

		random.shuffle(data_moments_indexed_loaded)

		print(timer.time(),len(data_moments_indexed_loaded))
		print(len(P['Loaded_image_files']))


	def _close_image_files():
		spd2s('_close_image_files()')
		for f in P['Loaded_image_files']:
			#spd2s(f)
			try:
				P['Loaded_image_files'][f]['normal'].close()
				P['Loaded_image_files'][f]['flip'].close()
			except Exception as e:
				print("********** _close_image_files Exception ***********************")
				print(e.message, e.args)




	def _function_fill(*args):

		global long_ctr,data_moments_indexed_loaded,reload_image_file_timer

		Args = args_to_dictionary(args)
		True

		if reload_image_file_timer.check():
			_close_image_files()
			_load_image_files()
			reload_image_file_timer.reset()

		D[data_ids] = []
		ctr = 0
		while ctr < D[batch_size]:
			if long_ctr == -1 or long_ctr >= len(data_moments_indexed_loaded):
				long_ctr = 0
				random.shuffle(data_moments_indexed_loaded)
				spd2s('random.shuffle(data_moments_indexed_loaded)')
			
			
			#b_ = ctr
			FLIP = random.choice([0,1])
			dm = data_moments_indexed_loaded[long_ctr]; long_ctr += 1; ctr += 1
			
			if True:#dm['run_name'] in P['Loaded_image_files']:

				#if (is_even(long_ctr) and dm['other_car_in_view'] == True) or ((not is_even(long_ctr)) and dm['other_car_in_view'] == False):
				if True:#dm['other_car_in_view'] == True:


					Data_moment = {}

					Data_moment['steer'] = zeros(90) + dm['steer']
					if FLIP:
						Data_moment['steer'] = 99 - Data_moment['steer']
					new_motor = dm['motor']
					new_motor -= 49
					new_motor = max(0,new_motor)
					new_motor *= 7.0
					Data_moment['motor'] = zeros(90) + new_motor
					Data_moment['labels'] = {}
					for l in ['direct','follow','clockwise','counter-clockwise']:
						Data_moment['labels'][l] = 0
					Data_moment['name'] = dm['run_name']
					direction = dm['counter_clockwise']
					behavioral_mode = dm['behavioral_mode']
					if behavioral_mode == 'Direct_Arena_Potential_Field':
						Data_moment['labels']['direct'] = 1
					elif behavioral_mode == 'Follow_Arena_Potential_Field':
						Data_moment['labels']['follow'] = 1

					if not FLIP:
						if direction == CLOCKWISE:
							Data_moment['labels']['clockwise'] = 1
						elif direction == COUNTER_C:
							Data_moment['labels']['counter-clockwise'] = 1
					else:
						if direction == COUNTER_C:
							Data_moment['labels']['clockwise'] = 1
						elif direction == CLOCKWISE:
							Data_moment['labels']['counter-clockwise'] = 1

					tl0 = dm['left_ts_index'][0]; il0 = dm['left_ts_index'][1]
					tr0 = dm['right_ts_index'][0]; ir0 = dm['right_ts_index'][1]


					if FLIP:
						F = P['Loaded_image_files'][Data_moment['name']]['flip']
					else:
						F = P['Loaded_image_files'][Data_moment['name']]['normal']

					Data_moment[left] = {}
					Data_moment[right] = {}



					if not FLIP:
						if il0+1 < len(F[left_image][vals]) and ir0+1 < len(F[right_image][vals]):
							Data_moment[left][0] = F[left_image][vals][il0]
							Data_moment[right][0] = F[right_image][vals][ir0]
							Data_moment[left][1] = F[left_image][vals][il0+1] # note, ONE frame
							Data_moment[right][1] = F[right_image][vals][ir0+1]
						else:
							spd2s('if il0+1 < len(F[left_image][vals]) and ir0+1 < len(F[right_image][vals]): NOT TRUE!')
							continue
					else:
						if il0+1 < len(F[left_image_flip][vals]) and ir0+1 < len(F['right_image_flip'][vals]):
							Data_moment[right][0] = F[left_image_flip][vals][il0]
							Data_moment[left][0] = F['right_image_flip'][vals][ir0]
							Data_moment[right][1] = F[left_image_flip][vals][il0+1]
							Data_moment[left][1] = F['right_image_flip'][vals][ir0+1]
						else:
							spd2s('if il0+1 < len(F[left_image_flip][vals]) and ir0+1 < len(F[right_image_flip][vals]): NOT TRUE!')
							continue
					ctr += 1

					_function_data_into_batch(data_moment,Data_moment)
					frequency_timer.freq()



	def _function_data_into_batch(*args):
		global img_juggled
		Args = args_to_dictionary(args)
		Data_moment = Args[data_moment]
		True
		if True:
			D['names'].insert(0,Data_moment[name]) # This to match torch.cat use below
		if True:
			offset = np.random.randint(20)
			list_camera_input = []
			for t in range(D['network'][net].N_FRAMES):
				for camerav in (left, right):
					img = Data_moment[camerav][t]#[40:,:,:]
					#if type(img_juggled) == int:
					#	img_juggled = img.copy()
					#new_order = [0,1,2]
					#random.shuffle(new_order)
					#for i in range(3):
					#	img_juggled[:,:,i] = img[:,:,new_order[i]] 
					img[:(30+offset),:,:] = 128
					#mci(img,title='_function_data_into_batch')
					list_camera_input.append(torch.from_numpy(img))
			camera_datav = torch.cat(list_camera_input, 2)

			camera_datav = camera_datav.cuda().float()/255. - 0.5
			#camera_datav = camera_datav.cuda().float()

			camera_datav = torch.transpose(camera_datav, 0, 2)
			camera_datav = torch.transpose(camera_datav, 1, 2)
			D['camera_data'] = torch.cat((torch.unsqueeze(camera_datav, 0), D['camera_data']), 0)


		"""
		# previous version
		if True:
			list_camera_input = []
			for t in range(D['network'][net].N_FRAMES):
				for camerav in (left, right):
					list_camera_input.append(torch.from_numpy(Data_moment[camerav][t]))
			camera_datav = torch.cat(list_camera_input, 2)
			camera_datav = camera_datav.cuda().float()/255. - 0.5
			camera_datav = torch.transpose(camera_datav, 0, 2)
			camera_datav = torch.transpose(camera_datav, 1, 2)
			D['camera_data'] = torch.cat((torch.unsqueeze(camera_datav, 0), D['camera_data']), 0)


		"""

		if True:
			mode_ctrv = 0
			metadatav = torch.FloatTensor().cuda()
			zero_matrixv = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()
			one_matrixv = torch.FloatTensor(1, 1, 23, 41).fill_(1).cuda()
			for cur_labelv in ['follow', 'direct','clockwise','counter-clockwise']:

				if cur_labelv in Data_moment[labels]:

					if Data_moment[labels][cur_labelv]:
						
						metadatav = torch.cat((one_matrixv, metadatav), 1);mode_ctrv += 1
					else:
						metadatav = torch.cat((zero_matrixv, metadatav), 1);mode_ctrv += 1

			"""
			if LCR in Data_moment[labels]:
				#print data[''states'']
				for target_statev in [1,2,3]:
					for i in range(0,len(Data_moment['states']),3): ###############!!!!!!!!!!!!!!!! temp, generalize
						mode_ctrv += 1
						#!!!!!!!! reverse concatinations so they are in normal order
						if Data_moment['states'][i] == target_statev:
							metadatav = torch.cat((one_matrixv, metadatav), 1)
						else:
							metadatav = torch.cat((zero_matrixv, metadatav), 1)
			"""
			#print 128-mode_ctrv,mode_ctrv
			for i in range(128 - mode_ctrv): # Concatenate zero matrices to fit the dataset
				metadatav = torch.cat((zero_matrixv, metadatav), 1)

			D['metadata'] = torch.cat((metadatav, D['metadata']), 0)

		if True:
			sv = Data_moment['steer']
			mv = Data_moment['motor']
			rv = range(8,91,9)
			#rv = range(2,31,3) # This depends on NUM_STEPS and STRIDE
			sv = array(sv)[rv]
			mv = array(mv)[rv]
			steerv = torch.from_numpy(sv).cuda().float() / 99.
			motorv = torch.from_numpy(mv).cuda().float() / 99.
			target_datav = torch.unsqueeze(torch.cat((steerv, motorv), 0), 0)
			D['target_data'] = torch.cat((target_datav, D['target_data']), 0)
			#D['states'].append(Data_moment['states'])



	def _function_clear():
		D['camera_data'] = torch.FloatTensor().cuda()
		D['metadata'] = torch.FloatTensor().cuda()
		D['target_data'] = torch.FloatTensor().cuda()
		D['states'] = []
		D['names'] = []
		D['outputs'] = None
		D['loss'] = None



	def _function_forward():
		True
		Trial_loss_record = D['network'][data_moment_loss_record]
		D['network'][optimizer].zero_grad()
		D['outputs'] = D['network'][net](torch.autograd.Variable(D['camera_data']), torch.autograd.Variable(D['metadata'])).cuda()
		D['loss'] = D['network'][criterion](D['outputs'], torch.autograd.Variable(D['target_data']))
		"""
		for bv in range(D[batch_size]):
			id = D[data_ids][bv]
			tv= D['target_data'][bv].cpu().numpy()
			ov = D['outputs'][bv].data.cpu().numpy()
			av = tv - ov
			#Trial_loss_record[(id,tuple(tv),tuple(ov))] = np.sqrt(av * av).mean()
			Trial_loss_record[id] = np.sqrt(av * av).mean()
		D['network'][rate_counter][step]()
		"""


	def _function_backward():
		True
		D['loss'].backward()
		nnutils.clip_grad_norm(D['network'][net].parameters(), 1.0)
		D['network'][optimizer].step()
		P['LOSS_LIST'].append(D['loss'].data.cpu().numpy()[:].mean())
		if len(P['LOSS_LIST']) > P['LOSS_LIST_N']:
			P['LOSS_LIST_AVG'].append(na(P['LOSS_LIST']).mean())
			P['LOSS_LIST'] = []


	def _function_display(*args):
		Args = args_to_dictionary(args)
		if print_now not in Args:
			Args[print_now] = False
		True
		cv2.waitKey(1) # This is to keep cv2 windows alive
		if P[print_timer].check() or Args[print_now]:

			ov = D['outputs'][0].data.cpu().numpy()
			mv = D['metadata'][0].cpu().numpy()
			tv = D['target_data'][0].cpu().numpy()

			print('Loss:',dp(D['loss'].data.cpu().numpy()[0],5))
			#print(o,t,D['data_ids'])
			av = D['camera_data'][0][:].cpu().numpy()
			bv = av.transpose(1,2,0)
			hv = shape(av)[1]
			wv = shape(av)[2]
			cv = zeros((10+hv*2,10+2*wv,3))
			cv[:hv,:wv,:] = z2o(bv[:,:,3:6])
			cv[:hv,-wv:,:] = z2o(bv[:,:,:3])
			cv[-hv:,:wv,:] = z2o(bv[:,:,9:12])
			cv[-hv:,-wv:,:] = z2o(bv[:,:,6:9])
			#mi(cv,'cameras');pause(0.000000001)
			print(d2s('camera_data min,max =',av.min(),av.max()))
			#print(D['states'][-1])
			#print shape(mv)
			#img_saver['save']({'img':c})
			if loss_timer.check():
				figure('LOSS_LIST_AVG');clf();plot(P['LOSS_LIST_AVG'],'.')
				spause()
				loss_timer.reset()
			Net_activity = Activity_Module.Net_Activity('activiations',D['network']['net'].A)

			Net_activity['view']('moment_index',0,'delay',33, 'scales',{'camera_input':3,'pre_metadata_features':0,'pre_metadata_features_metadata':2,'post_metadata_features':4})

			if mv[-1,0,0]:
				bm = 'follow'
			elif mv[-2,0,0]:
				bm = 'direct'
			else:
				assert(False)
			if mv[-3,0,0]:
				dr = 'clockwise'
			elif mv[-4,0,0]:
				dr = 'counter-clockwise'
			else:
				assert(False)				
			

			figure('steer')
			clf()
			ylim(-0.05,1.05);xlim(0,len(tv))
			plot([-1,10],[0.49,0.49],'k');plot(ov,'og'); plot(tv,'or'); plt.title(D['names'][0])
			plt.xlabel(d2s(bm,dr))

			figure('metadata');clf()
			plot(mv[-10:,0,0],'r.-')
			plt.title(d2s(bm,dr))


			spause()

			P[print_timer].reset()
	"""
	
	"""

	D['FILL'] = _function_fill
	D['CLEAR'] = _function_clear
	D['FORWARD'] = _function_forward
	D['BACKWARD'] = _function_backward
	D['DISPLAY'] = _function_display
	return D


#scales,{camera_input:2,post_metadata_features:4,pre_metadata_features:1},

#EOF
