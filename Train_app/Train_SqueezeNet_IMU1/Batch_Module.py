from Parameters_Module import *
exec(identify_file_str)
from vis2 import *
import torch
import torch.nn.utils as nnutils
import Activity_Module

control_filter1 = zeros(90); control_filter1[:5] = 1.0; control_filter1[5:10] = 0.5
control_filter2 = 1.0/((arange(90)/60.0)**2+1.0); control_filter2[:5] = 0.0; control_filter2[5:10] = 0.5

data_moments_indexed = P['data_moments_indexed']

DIRECT = 'Direct_Arena_Potential_Field'
FOLLOW = 'Follow_Arena_Potential_Field'
CLOCKWISE = 0
COUNTER_C = 1
long_ctr = -1
P['LOSS_LIST'] = []
P['LOSS_LIST_AVG'] = []

loss_timer = Timer(60*5)

frequency_timer = Timer(10.0)

INTO_TORCH = 1

def Batch(**Args):
	_ = {}
	_[network] = Args[network]
	True
	_[BATCH_SIZE] = P[BATCH_SIZE]
	_[dic_type] = 'Batch'
	_[purpose] = d2s(inspect.stack()[0][3],':','object to collect data for pytorch batch')
	_[CAMERA_DATA] = torch.FloatTensor().cuda()
	_[metadata] = torch.FloatTensor().cuda()
	_[target_data] = torch.FloatTensor().cuda()
	_[names] = []
	_[states] = []

	DIRECT = 'Direct_Arena_Potential_Field'
	FOLLOW = 'Follow_Arena_Potential_Field'
	CLOCKWISE = 0
	COUNTER_C = 1

	def _function_fill(**Args):
		global long_ctr,data_moments_indexed		

		True
		_[data_ids] = []
		ctr = 0
		while ctr < _[BATCH_SIZE]:
			#print ctr
			if True:#try:
				if long_ctr == -1 or long_ctr >= len(data_moments_indexed):
					long_ctr = 0
					random.shuffle(data_moments_indexed)
					spd2s('suffle data_moments_indexed, len =',len(data_moments_indexed))
				b_ = ctr
				FLIP = random.choice([0,1])
				dm = data_moments_indexed[long_ctr]; long_ctr += 1; #ctr += 1
				Data_moment = {}

				Data_moment['steer'] = zeros(90) + dm[3][0]
				if FLIP:
					Data_moment['steer'] = 99 - Data_moment['steer']
				new_motor = dm[3][1]
				new_motor -= 49
				new_motor = max(0,new_motor)
				new_motor *= 7.0
				Data_moment['motor'] = zeros(90) + new_motor#dm[3][1]
				Data_moment['labels'] = {}
				for l in ['direct','follow','clockwise','counter-clockwise']:
					Data_moment['labels'][l] = 0
				Data_moment['name'] = dm[0]
				if Data_moment['name'] not in P['All_image_files']:
					continue
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

				Data_moment['labels']['counter-clockwise'] = 0 #!!!!!!!!!!!!!!!!!!!!!!!!!
				Data_moment['labels']['clockwise'] = 0 #!!!!!!!!!!!!!!!!!!!!!!!!!!!

				tl0 = dm[1][0][0]; il0 = dm[1][0][1]
				tr0 = dm[1][1][0]; ir0 = dm[1][1][1]

				if FLIP:
					F = P['All_image_files'][Data_moment['name']]['flip']
				else:
					F = P['All_image_files'][Data_moment['name']]['normal']

				Data_moment[left] = {}
				Data_moment[right] = {}

				if not FLIP:
					for q in range(_[network][net].N_FRAMES):
						Data_moment[left][q] = F[left_image][vals][il0+q]
						Data_moment[right][q] = F[right_image][vals][ir0+q]
						#print('\t\ta')
				else:
					for q in range(_[network][net].N_FRAMES):
						Data_moment[right][q] = F[left_image_flip][vals][il0+q]
						Data_moment[left][q] = F['right_image_flip'][vals][ir0+q]
						#print('\t\tb')

				_function_data_into_batch(data_moment=Data_moment)
				ctr += 1
				#pd2s('ctr =',ctr)
				frequency_timer.freq()
			else: #except:
				print('def _function_fill(*args):')


	def _function_data_into_batch(**Args):
		Data_moment = Args[data_moment]
		True
		if True:
			_[names].insert(0,Data_moment[name]) # This to match torch.cat use below
		if INTO_TORCH:
			offset = np.random.randint(20)
			list_camera_input = []
			for t in range(_[network][net].N_FRAMES):
				#pd2s('\t',t)
				for camerav in (left, right):
					img = Data_moment[camerav][t]#[40:,:,:]
					img[:(30+offset),:,:] = 128
					list_camera_input.append(torch.from_numpy(img))
			#pd2s('shape(list_camera_input) =',shape(list_camera_input))
			camera_data = torch.cat(list_camera_input, 2)
			camera_data = camera_data.cuda().float()/255. - 0.5
			camera_data = torch.transpose(camera_data, 0, 2)
			camera_data = torch.transpose(camera_data, 1, 2)
			_[CAMERA_DATA] = torch.cat((torch.unsqueeze(camera_data, 0), _[CAMERA_DATA]), 0)

		if INTO_TORCH:
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


			for i in range(128 - mode_ctrv): # Concatenate zero matrices to fit the dataset
				metadatav = torch.cat((zero_matrixv, metadatav), 1)

			_[metadata] = torch.cat((metadatav, _[metadata]), 0)

		if INTO_TORCH:
			sv = Data_moment[steer]
			mv = Data_moment[motor]
			rv = range(8,91,9)
			sv = array(sv)[rv]
			mv = array(mv)[rv]
			steerv = torch.from_numpy(sv).cuda().float() / 99.
			motorv = torch.from_numpy(mv).cuda().float() / 99.
			target_datav = torch.unsqueeze(torch.cat((steerv, motorv), 0), 0)
			_[target_data] = torch.cat((target_datav, _[target_data]), 0)


	def _function_clear():
		_[CAMERA_DATA] = torch.FloatTensor().cuda()
		_[metadata] = torch.FloatTensor().cuda()
		_[target_data] = torch.FloatTensor().cuda()
		_[states] = []
		_[names] = []
		_[outputs] = None
		_[loss] = None


	def _function_forward():
		True
		Trial_loss_record = _[network][data_moment_loss_record]
		_[network][optimizer].zero_grad()
		_[outputs] = _[network][net](torch.autograd.Variable(_[CAMERA_DATA]), torch.autograd.Variable(_[metadata])).cuda()
		_[loss] = _[network][criterion](_[outputs], torch.autograd.Variable(_[target_data]))


	def _function_backward():
		True
		_[loss].backward()
		nnutils.clip_grad_norm(_[network][net].parameters(), 1.0)
		_[network][optimizer].step()
		P['LOSS_LIST'].append(_[loss].data.cpu().numpy()[:].mean())
		if len(P['LOSS_LIST']) > 100:
			P['LOSS_LIST_AVG'].append(na(P['LOSS_LIST']).mean())
			P['LOSS_LIST'] = []


	def _function_display(*args):
		Args = args_to_dictionary(args)
		if print_now not in Args:
			Args[print_now] = False
		True
		cv2.waitKey(1) # This is to keep cv2 windows alive
		if P[print_timer].check() or Args[print_now]:

			ov = _[outputs][0].data.cpu().numpy()
			mv = _[metadata][0].cpu().numpy()
			tv = _[target_data][0].cpu().numpy()

			print('Loss:',dp(_[loss].data.cpu().numpy()[0],5))

			if loss_timer.check():
				figure('LOSS_LIST_AVG');clf();plot(P['LOSS_LIST_AVG'],'.')
				loss_timer.reset()

			Net_activity = Activity_Module.Net_Activity(activiations,_[network][net].A)
			Net_activity[view](moment_index,0,delay,33, scales,{camera_input:3,pre_metadata_features:0,pre_metadata_features_metadata:2,post_metadata_features:4})

			figure('steer')
			clf()
			ylim(-0.05,1.05);xlim(0,len(tv))
			plot([-1,60],[0.49,0.49],'k');plot(ov,'og'); plot(tv,'or'); plt.title(_[names][0])
			figure('metadata');clf()
			plot(mv[-10:,0,0],'r.-')
			spause()

			P[print_timer].reset()


	_[FILL] = _function_fill
	_[CLEAR] = _function_clear
	_[FORWARD] = _function_forward
	_[BACKWARD] = _function_backward
	_[DISPLAY] = _function_display
	return _



#EOF
