from Data_Moment_Module import *
from kzpy3.vis3 import *
import torch
import torch.nn.utils as nnutils
import Activity_Module
exec(identify_file_str)

P['metadata_constant_blanks'] = False
P['metadata_constant_gradients'] = False
P['long_ctr'] = -1
P['LOSS_LIST'] = []
if 'LOSS_LIST_AVG' not in P:
	P['LOSS_LIST_AVG'] = []
P['reload_image_file_timer'].trigger()
zero_matrix = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()
one_matrix = torch.FloatTensor(1, 1, 23, 41).fill_(1).cuda()
fill_once = False


def Batch(the_network=None):
	D = {}
	D['network'] = the_network
	D['batch_size'] = P['BATCH_SIZE']
	D['camera_data'] = torch.FloatTensor().cuda()
	D['metadata'] = torch.FloatTensor().cuda()
	D['target_data'] = torch.FloatTensor().cuda()
	D['names'] = []
	D['flips'] = []
	D['states'] = []
	D['tries'] = 0
	D['successes'] = 0
	D['zeros, metadata_size'] = zeros((1,1,23,41))


	def _function_fill():

		ctr = 0


		while ctr < D['batch_size']:
			if True:#try:
				
				Data_moment = get_Data_moment()

				ctr += 1

				D['names'].insert(0,Data_moment['name']) # This to match torch.cat use below
				D['flips'].insert(0,Data_moment['FLIP']) # This to match torch.cat use below

				list_camera_input = []
				for t in range(D['network']['net'].N_FRAMES):
					for camera in ('left', 'right'):
						list_camera_input.append(torch.from_numpy(Data_moment[camera][t]))
						#cy(shape(Data_moment[camera][t]))
				camera_data = torch.cat(list_camera_input, 2)

				#cg(camera_data.size())
				camera_data = camera_data.cuda().float()/255.-0.5
				#cy(camera_data.size())
				camera_data = torch.transpose(camera_data, 0, 2)
				#cb(camera_data.size())
				camera_data = torch.transpose(camera_data, 1, 2)
				#cr(camera_data.size())
				D['camera_data'] = torch.cat((torch.unsqueeze(camera_data, 0), D['camera_data']), 0)





				if type(P['metadata_constant_blanks']) == type(False):
					assert P['metadata_constant_blanks'] == False
					cr("************* making metadata_constant *************")

					mode_ctr = len(Data_moment['labels'])
					metadata_constant = torch.FloatTensor().cuda()
					num_metadata_channels = 128
					num_multival_metas = 1 + 4 + 12 #+ 27
					for i in range(num_metadata_channels - num_multival_metas - mode_ctr): # Concatenate zero matrices to fit the dataset
						metadata_constant = torch.cat((zero_matrix, metadata_constant), 1)
					P['metadata_constant_blanks'] = metadata_constant

					metadata_constant = torch.FloatTensor().cuda()
					meta_gradient1 = zero_matrix.clone()
					for x in range(23):
						meta_gradient1[:,:,x,:] = x/23.0
					metadata_constant = torch.cat((meta_gradient1, metadata_constant), 1)

					meta_gradient2 = zero_matrix.clone()
					for x in range(23):
						meta_gradient2[:,:,x,:] = (1.0-x/23.0)
					metadata_constant = torch.cat((meta_gradient2, metadata_constant), 1)

					meta_gradient3 = zero_matrix.clone()
					for x in range(41):
						meta_gradient3[:,:,:,x] = x/41.0
					metadata_constant = torch.cat((meta_gradient3, metadata_constant), 1)

					meta_gradient4 = zero_matrix.clone()
					for x in range(41):
						meta_gradient4[:,:,:,x] = (1.0-x/41.0)
					metadata_constant = torch.cat((meta_gradient4, metadata_constant), 1)
					P['metadata_constant_gradients'] = metadata_constant

				cat_list = [P['metadata_constant_gradients']]

							
				for t in range(D['network']['net'].N_FRAMES):
					for camera in ('left_small', 'right_small'):
						for color in [0,1,2]: 
							img = Data_moment[camera][t][:,:,color]
							
							img0 = D['zeros, metadata_size']
							img0[0,0,:,:] = img
							img1 = torch.from_numpy(img0)
							img2 = img1.cuda().float()/255.-0.5
							cat_list.append(img2)
				
				cat_list.append(P['metadata_constant_blanks'])

				metadata_I = torch.cat(cat_list, 1)

				metadata = torch.FloatTensor().cuda()

				for cur_label in P['behavioral_modes']:

					if cur_label in Data_moment['labels']:

						if Data_moment['labels'][cur_label]:
							
							metadata = torch.cat((one_matrix, metadata), 1);#mode_ctr += 1
						else:
							metadata = torch.cat((zero_matrix, metadata), 1);#mode_ctr += 1
					else:
						metadata = torch.cat((zero_matrix, metadata), 1);#mode_ctr += 1

				metadata = torch.cat((metadata_I, metadata), 1)

				for topic in ['encoder']:#,'acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z','encoder']:
					meta_gradient5 = zero_matrix.clone()
					d = Data_moment[topic+'_past']/100.0
					if topic == 'encoder':
						med = np.median(d)
						for i in range(len(d)):
							if d[i] < med/3.0:
								d[i] = med # this to attempt to get rid of drop out from magnet not being read
						d = d/5.0
					d = d.reshape(-1,3).mean(axis=1)
					for x in range(0,23):
						meta_gradient5[:,:,x,:] = d[x]
					metadata = torch.cat((meta_gradient5, metadata), 1)

				D['metadata'] = torch.cat((metadata, D['metadata']), 0)

				sv = Data_moment['steer']
				mv = Data_moment['motor']
				hv = Data_moment['gyro_heading_x']
				ev = Data_moment['encoder_meo']

				rv = P['prediction_range']

				sv = array(sv)[rv]
				mv = array(mv)[rv]
				hv = array(hv)[rv]
				ev = array(ev)[rv]

				for q in rlen(mv):
					if mv[q] < 49:
						ev[q] *= -1

				hv = hv - hv[0]

				steer = torch.from_numpy(sv).cuda().float() / 99.
				motor = torch.from_numpy(mv).cuda().float() / 99.
				heading = (torch.from_numpy(hv).cuda().float()) / 90.0
				encoder = (torch.from_numpy(ev).cuda().float()) / 5.0
				target_data = torch.unsqueeze(torch.cat((steer,motor,heading,encoder), 0), 0)
				D['target_data'] = torch.cat((target_data, D['target_data']), 0)

				P['frequency_timer'].freq(d2s('train duration =',int(P['duration timer'].time()),"\t"))



			else: #except Exception as e:
				print("*** while ctr < D['batch_size']: ******* Exception ***********************")
				print(e.message, e.args)



	def _function_clear():
		D['camera_data'] = torch.FloatTensor().cuda()
		D['metadata'] = torch.FloatTensor().cuda()
		D['target_data'] = torch.FloatTensor().cuda()
		D['states'] = []
		D['names'] = []
		D['outputs'] = None
		D['loss'] = None


	def _function_forward():
		D['network']['optimizer'].zero_grad()
		D['outputs'] = D['network']['net'](torch.autograd.Variable(D['camera_data']), torch.autograd.Variable(D['metadata'])).cuda()
		D['loss'] = D['network']['criterion'](D['outputs'], torch.autograd.Variable(D['target_data']))


	def _function_backward():
		try:
			D['tries'] += 1
			D['loss'].backward()
			nnutils.clip_grad_norm(D['network']['net'].parameters(), 1.0)
			D['network']['optimizer'].step()
			
			P['LOSS_LIST'].append(D['loss'].data.cpu().numpy()[:].mean())

			if len(P['LOSS_LIST']) > P['LOSS_LIST_N']:
				P['LOSS_LIST_AVG'].append(na(P['LOSS_LIST']).mean())
				P['LOSS_LIST'] = []
			D['successes'] += 1

		except Exception as e:
			print("********** Exception ****** def _function_backward(): failed!!!! *****************")
			print(e.message, e.args)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			CS_('Exception!',exception=True,newline=False)
			CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
			pd2s( D['tries'],D['successes'],int(100*D['successes']/(1.0*D['tries'])),"percent successes" )
			




	def _function_display():
		cv2.waitKey(1) # This is to keep cv2 windows alive
		if P['print_timer'].check():
			cprint(d2s("P['start time'] =",P['start time']),'blue','on_yellow')
			for i in [0]:#range(P['BATCH_SIZE']):
				ov = D['outputs'][i].data.cpu().numpy()
				mv = D['metadata'][i].cpu().numpy()
				tv = D['target_data'][i].cpu().numpy()
				cg("len(ov),len(tv) =", len(ov),len(tv))
				#raw_enter()
				if P['verbose']: print('Loss:',dp(D['loss'].data.cpu().numpy()[0],5))
				av = D['camera_data'][i][:].cpu().numpy()
				bv = av.transpose(1,2,0)
				hv = shape(av)[1]
				wv = shape(av)[2]
				cv = zeros((10+hv*2,10+2*wv,3))
				cv[:hv,:wv,:] = z2o(bv[:,:,3:6])
				cv[:hv,-wv:,:] = z2o(bv[:,:,:3])
				cv[-hv:,:wv,:] = z2o(bv[:,:,9:12])
				cv[-hv:,-wv:,:] = z2o(bv[:,:,6:9])
				if P['verbose']: print(d2s(i,'camera_data min,max =',av.min(),av.max()))
				
				Net_activity = Activity_Module.Net_Activity('batch_num',i, 'activiations',D['network']['net'].A)
				Net_activity['view']('moment_index',i,'delay',33, 'scales',{'camera_input':4,'pre_metadata_features':0,'pre_metadata_features_metadata':1,'post_metadata_features':0})
				bm = 'unknown behavioral_mode'
				for j in range(len(P['behavioral_modes'])):
					if mv[-(j+1),0,0]:
						bm = P['behavioral_modes'][j]
					#else:
					#	cr(P['behavioral_modes'][j],'unknown behavioral_mode !!!')
				figure('steer '+P['start time'])
				clf()
				plt.title(d2s(i))
				ylim(-1.05,1.05);xlim(0,len(tv))
				plot([-1,20],[0.49,0.49],'k');
				plot([-1,20],[0.0,0.0],'k')
				plot(ov,'og'); plot(tv,'or'); plt.title(D['names'][0])
				if D['flips'][0]:
					flip_str = '(flip)'
				else:
					flip_str = ''
				plt.xlabel(d2s(bm,flip_str))
				if False:
					figure('metadata '+P['start time']);clf()
					plot(mv[-10:,0,0],'r.-')
					plt.title(d2s(bm,i))
				spause()
				P['print_timer'].reset()
			dm_ctrs_max = 100
			dm_ctrs = zeros(dm_ctrs_max)
			loss_list = []
			for j in range(len(P['data_moments_indexed'])):
				if 'ctr' in P['data_moments_indexed'][j]:
					k = P['data_moments_indexed'][j]['ctr']
					if k < dm_ctrs_max:
						dm_ctrs[k] += 1
				else:
					dm_ctrs[0] += 1
				if 'loss' in P['data_moments_indexed'][j]:
					if len(P['data_moments_indexed'][j]['loss']) > 0:
						loss_list.append(P['data_moments_indexed'][j]['loss'][-1])
			if False:
				figure('dm_ctrs '+P['start time']);clf();plot(dm_ctrs,'.-');xlim(0,100)
			P['dm_ctrs'] = dm_ctrs
			#figure('loss_list');clf();hist(loss_list)
			spause()

			if bm == 'unknown behavioral_mode':
				raw_enter()

		if P['loss_timer'].check() and len(P['LOSS_LIST_AVG'])>5:
			q = int(len(P['LOSS_LIST_AVG'])*P['percent_of_loss_list_avg_to_show']/100.0)
			figure('LOSS_LIST_AVG '+P['start time']);clf();plot(P['LOSS_LIST_AVG'][-q:],'.')
			u = min(len(P['LOSS_LIST_AVG']),250)
			median_val = np.median(na(P['LOSS_LIST_AVG'][-u:]))
			plt.title(d2s('median =',dp(median_val,6)))
			plot([0,q],[median_val,median_val],'r')
			plt.xlim(0,q)
			spause()
			P['loss_timer'].reset()

	D['FILL'] = _function_fill
	D['CLEAR'] = _function_clear
	D['FORWARD'] = _function_forward
	D['BACKWARD'] = _function_backward
	D['DISPLAY'] = _function_display

	return D






#EOF
