from Parameters_Module import *
exec(identify_file_str)
from kzpy3.vis2 import *
import torch
import torch.nn.utils as nnutils
import Activity_Module

#img_saver = Image_to_Folder_Saver({'path':opjD('cameras0')})

_ = dictionary_access

#Aruco_Steering_Trajectories = h5r(opj(P['BAIR_CAR_DATA_PATH'],'Aruco_Steering_Trajectories.hdf5'))
"""
def load_Aruco_Steering_Trajectories():
	print("Loading Aruco_Steering_Trajectories . . .")
	paths = sggo(opjD('Aruco_Steering_Trajectories','*.pkl'))
	Aruco_Steering_Trajectories = {}
	ctr = 0
	for p in paths:
		o = lo(p)
		run_name = fname(p).replace('.pkl','')
		print(d2n(run_name,' (',ctr+1,' of ',len(paths),')'))
		Aruco_Steering_Trajectories[run_name] = o
		ctr += 1
	return Aruco_Steering_Trajectories

P['Aruco_Steering_Trajectories']['Direct_Arena_Potential_Field'][0]['flip_caffe2_z2_color_direct_Smyth_tape_02Mar17_16h26m00s_Mr_Orange']


if True:
	Aruco_Steering_Trajectories = load_Aruco_Steering_Trajectories()
"""
#Aruco_Steering_Trajectories = P['Aruco_Steering_Trajectories']#lo(opj(P[BAIR_CAR_DATA_PATH],'Aruco_Steering_Trajectories'))



control_filter1 = zeros(90); control_filter1[:5] = 1.0; control_filter1[5:10] = 0.5
control_filter2 = 1.0/((arange(90)/60.0)**2+1.0); control_filter2[:5] = 0.0; control_filter2[5:10] = 0.5




All_image_files = P['All_image_files']
data_moments_indexed = P['data_moments_indexed']

DIRECT = 'Direct_Arena_Potential_Field'
FOLLOW = 'Follow_Arena_Potential_Field'
CLOCKWISE = 0
COUNTER_C = 1
long_ctr = -1

frequency_timer = Timer(10.0)
def Batch(*args):
	Args = args_to_dictionary(args)
	D = {}
	D[network] = Args[network]
	True
	_(D,batch_size,equals,P[BATCH_SIZE])
	D[dic_type] = 'Batch'
	D[purpose] = d2s(inspect.stack()[0][3],':','object to collect data for pytorch batch')
	D[camera_data] = torch.FloatTensor().cuda()
	D[metadata] = torch.FloatTensor().cuda()
	D[target_data] = torch.FloatTensor().cuda()
	D[names] = []
	D[states] = []

	DIRECT = 'Direct_Arena_Potential_Field'
	FOLLOW = 'Follow_Arena_Potential_Field'
	CLOCKWISE = 0
	COUNTER_C = 1

	def _function_fill(*args):
		#print 'AAAAAAAAAAAAAAAAAAAA'
		global long_ctr,data_moments_indexed
		#print long_ctr
		if long_ctr == -1 or long_ctr >= len(data_moments_indexed):
			long_ctr = 0
			random.shuffle(data_moments_indexed)

		Args = args_to_dictionary(args)
		True
		D[data_ids] = []
		ctr = 0
		while ctr < D[batch_size]:
			frequency_timer.freq()
			#pd2s('ctr =',ctr)
			b_ = ctr
			FLIP = random.choice([0,1])
			dm = data_moments_indexed[long_ctr]; long_ctr += 1; ctr += 1
			#print dm
			Data_moment = {}

			Data_moment['steer'] = zeros(90) + dm[3][0]
			if FLIP:
				Data_moment['steer'] = 99 - Data_moment['steer']
			Data_moment['motor'] = zeros(90) + dm[3][1]
			Data_moment['labels'] = {}
			for l in ['direct','follow','clockwise','counter-clockwise']:
				Data_moment['labels'][l] = 0
			Data_moment['name'] = dm[0]
			direction = dm[2][1]
			behavioral_mode = dm[2][0]
			if behavioral_mode == DIRECT:
				Data_moment['labels']['direct'] = 1
			elif behavioral_mode == FOLLOW:
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

			tl0 = dm[1][0][0]; il0 = dm[1][0][1]
			tr0 = dm[1][1][0]; ir0 = dm[1][1][1]

			if FLIP:
				F = All_image_files[Data_moment['name']]['flip']
			else:
				F = All_image_files[Data_moment['name']]['normal']

			Data_moment[left] = {}
			Data_moment[right] = {}

			if not FLIP:
				Data_moment[left][0] = F[left_image][vals][il0]
				Data_moment[right][0] = F[right_image][vals][ir0]
				Data_moment[left][1] = F[left_image][vals][il0+2] # note, two frames
				Data_moment[right][1] = F[right_image][vals][ir0+2]
			else:
				Data_moment[right][0] = F[left_image_flip][vals][il0]
				Data_moment[left][0] = F['right_image_flip'][vals][ir0]
				Data_moment[right][1] = F[left_image_flip][vals][il0+2]
				Data_moment[left][1] = F['right_image_flip'][vals][ir0+2]
			#mci(Data_moment[right][1],title='r1',delay=1)
			ctr += 1
			#D[data_ids].append((run_codev,seg_numv,offsetv))
			#print Data_moment['labels']
			_function_data_into_batch(data_moment,Data_moment)
		#D[data_ids].reverse() # this is to match way batch is filled up below


	def _function_data_into_batch(*args):
		Args = args_to_dictionary(args)
		Data_moment = Args[data_moment]
		True
		if True:
			D[names].insert(0,Data_moment[name]) # This to match torch.cat use below
		if True:
			offset = np.random.randint(20)
			list_camera_input = []
			for t in range(D[network][net].N_FRAMES):
				for camerav in (left, right):
					img = Data_moment[camerav][t]#[40:,:,:]
					img[:(30+offset),:,:] = 128
					#mci(img,title='_function_data_into_batch')
					list_camera_input.append(torch.from_numpy(img))
			camera_datav = torch.cat(list_camera_input, 2)
			camera_datav = camera_datav.cuda().float()/255. - 0.5
			camera_datav = torch.transpose(camera_datav, 0, 2)
			camera_datav = torch.transpose(camera_datav, 1, 2)
			D[camera_data] = torch.cat((torch.unsqueeze(camera_datav, 0), D[camera_data]), 0)


		"""
		# previous version
		if True:
			list_camera_input = []
			for t in range(D[network][net].N_FRAMES):
				for camerav in (left, right):
					list_camera_input.append(torch.from_numpy(Data_moment[camerav][t]))
			camera_datav = torch.cat(list_camera_input, 2)
			camera_datav = camera_datav.cuda().float()/255. - 0.5
			camera_datav = torch.transpose(camera_datav, 0, 2)
			camera_datav = torch.transpose(camera_datav, 1, 2)
			D[camera_data] = torch.cat((torch.unsqueeze(camera_datav, 0), D[camera_data]), 0)


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
				#print data['states']
				for target_statev in [1,2,3]:
					for i in range(0,len(Data_moment[states]),3): ###############!!!!!!!!!!!!!!!! temp, generalize
						mode_ctrv += 1
						#!!!!!!!! reverse concatinations so they are in normal order
						if Data_moment[states][i] == target_statev:
							metadatav = torch.cat((one_matrixv, metadatav), 1)
						else:
							metadatav = torch.cat((zero_matrixv, metadatav), 1)
			"""
			#print 128-mode_ctrv,mode_ctrv
			for i in range(128 - mode_ctrv): # Concatenate zero matrices to fit the dataset
				metadatav = torch.cat((zero_matrixv, metadatav), 1)

			D[metadata] = torch.cat((metadatav, D[metadata]), 0)

		if True:
			sv = Data_moment[steer]
			mv = Data_moment[motor]
			rv = range(8,91,9)
			#rv = range(2,31,3) # This depends on NUM_STEPS and STRIDE
			sv = array(sv)[rv]
			mv = array(mv)[rv]
			steerv = torch.from_numpy(sv).cuda().float() / 99.
			motorv = torch.from_numpy(mv).cuda().float() / 99.
			target_datav = torch.unsqueeze(torch.cat((steerv, motorv), 0), 0)
			D[target_data] = torch.cat((target_datav, D[target_data]), 0)
			#D[states].append(Data_moment[states])



	def _function_clear():
		D[camera_data] = torch.FloatTensor().cuda()
		D[metadata] = torch.FloatTensor().cuda()
		D[target_data] = torch.FloatTensor().cuda()
		D[states] = []
		D[names] = []
		D[outputs] = None
		D[loss] = None



	def _function_forward():
		True
		Trial_loss_record = D[network][data_moment_loss_record]
		D[network][optimizer].zero_grad()
		D[outputs] = D[network][net](torch.autograd.Variable(D[camera_data]), torch.autograd.Variable(D[metadata])).cuda()
		D[loss] = D[network][criterion](D[outputs], torch.autograd.Variable(D[target_data]))
		"""
		for bv in range(D[batch_size]):
			id = D[data_ids][bv]
			tv= D[target_data][bv].cpu().numpy()
			ov = D[outputs][bv].data.cpu().numpy()
			av = tv - ov
			#Trial_loss_record[(id,tuple(tv),tuple(ov))] = np.sqrt(av * av).mean()
			Trial_loss_record[id] = np.sqrt(av * av).mean()
		D[network][rate_counter][step]()
		"""


	def _function_backward():
		True
		D[loss].backward()
		nnutils.clip_grad_norm(D[network][net].parameters(), 1.0)
		D[network][optimizer].step()



	def _function_display(*args):
		Args = args_to_dictionary(args)
		if print_now not in Args:
			Args[print_now] = False
		True
		cv2.waitKey(1) # This is to keep cv2 windows alive
		if P[print_timer].check() or Args[print_now]:

			ov = D[outputs][0].data.cpu().numpy()
			mv = D[metadata][0].cpu().numpy()
			tv = D[target_data][0].cpu().numpy()

			print('Loss:',dp(D[loss].data.cpu().numpy()[0],5))
			#print(o,t,D['data_ids'])
			av = D[camera_data][0][:].cpu().numpy()
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
			#print(D[states][-1])
			#print shape(mv)
			#img_saver['save']({'img':c})


			Net_activity = Activity_Module.Net_Activity(activiations,D[network][net].A)

			Net_activity[view](moment_index,0,delay,33, scales,{camera_input:3,pre_metadata_features:0,pre_metadata_features_metadata:2,post_metadata_features:4})

			figure('steer')
			clf()
			ylim(-0.05,1.05);xlim(0,len(tv))
			plot([-1,60],[0.49,0.49],'k');plot(ov,'og'); plot(tv,'or'); plt.title(D[names][0])
			figure('metadata');clf()
			plot(mv[-10:,0,0],'r.-')
			spause()

			P[print_timer].reset()
	"""
	
	"""

	D[fill] = _function_fill
	D[clear] = _function_clear
	D[forward] = _function_forward
	D[backward] = _function_backward
	D[display] = _function_display
	return D


#scales,{camera_input:2,post_metadata_features:4,pre_metadata_features:1},

#EOF
