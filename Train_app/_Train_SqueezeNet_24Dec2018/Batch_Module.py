from Parameters_Module import *

exec(identify_file_str)
from kzpy3.vis3 import *
import torch
import torch.nn.utils as nnutils
import Activity_Module

P['data_moments_indexed_loaded'] = []
P['metadata_constant_blanks'] = False
P['metadata_constant_gradients'] = False
P['long_ctr'] = -1
P['LOSS_LIST'] = []
if 'LOSS_LIST_AVG' not in P:
	P['LOSS_LIST_AVG'] = []
P['reload_image_file_timer'].trigger()

zero_matrix = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()
one_matrix = torch.FloatTensor(1, 1, 23, 41).fill_(1).cuda()
temp = (255*z2o(np.random.randn(94,168))).astype(np.uint8)


def Batch(the_network=None):
	D = {}
	D['network'] = the_network
	True
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

	files = sggo('/home/karlzipser/Desktop/Data/Network_Predictions_projected/*.net_projections.h5py')
	GOOD_LIST = []
	for f in files:
	    GOOD_LIST.append(fname(f).split('.')[0])
    
	def _load_image_files():
		cy('_load_image_files()')
		P['Loaded_image_files'] = {}

		shuffled_keys = P['run_name_to_run_path'].keys()
		random.shuffle(shuffled_keys)

		for f in shuffled_keys[:P['max_num_runs_to_open']]:

			if f not in GOOD_LIST:
				continue

			P['Loaded_image_files'][f] = {}
			if True:
				try:

					L,O,F = open_run(run_name=f,h5py_path=pname(P['run_name_to_run_path'][f]))
					S = h5r(opjD('Data','Network_Predictions_projected',f+'.net_projections.h5py'))
					P['Loaded_image_files'][f]['normal'] = O
					P['Loaded_image_files'][f]['flip'] = F
					P['Loaded_image_files'][f]['left_timestamp_metadata'] = L
					P['Loaded_image_files'][f]['projections'] = S
					P['Loaded_image_files'][f]['normal projections'] = S['normal']
					P['Loaded_image_files'][f]['flip projections'] = S['flip']

					if P['use_LIDAR']:
						path = opj(P['LIDAR_path'],f+P['LIDAR_extension'])
						cg("*",path,"*")
						R = h5r(path)
						P['Loaded_image_files'][f]['depth'] = R

				except Exception as e:
					print("********** Exception ***********************")
					print(e.message, e.args)

		if P['verbose']: print(len(P['Loaded_image_files']))

		pd2s('1) len(P[data_moments_indexed]) =',len(P['data_moments_indexed']))

		timer = Timer()
		P['data_moments_indexed_loaded'] = []


		for dm in P['data_moments_indexed']:
			if dm['run_name'] in P['Loaded_image_files']:
				P['data_moments_indexed_loaded'].append(dm)

		random.shuffle(P['data_moments_indexed_loaded'])

		pd2s('index discovery time =',timer.time(),'len(P[data_moments_indexed_loaded]) =',len(P['data_moments_indexed_loaded']))
	






	def _close_image_files():

		cy('_close_image_files()')

		for f in P['Loaded_image_files']:

			try:
				P['Loaded_image_files'][f]['normal'].close()
				P['Loaded_image_files'][f]['flip'].close()

				P['Loaded_image_files'][f]['projections'].close()

				if P['use_LIDAR']:
					P['Loaded_image_files'][f]['depth'].close()

			except Exception as e:
				print("********** _close_image_files Exception ***********************")
				print(e.message, e.args)







	def _function_fill():

		if P['reload_image_file_timer'].check():
			_close_image_files()
			_load_image_files()
			P['reload_image_file_timer'].reset()

		ctr = 0
		P['current_batch'] = []
		while ctr < D['batch_size']:
			if True:#try:
				if P['long_ctr'] == -1 or P['long_ctr'] >= len(P['data_moments_indexed_loaded']):
					P['long_ctr'] = 0
					random.shuffle(P['data_moments_indexed_loaded'])
					cy('random.shuffle(P[data_moments_indexed_loaded])')
				
				FLIP = random.choice([0,1])
				dm = P['data_moments_indexed_loaded'][P['long_ctr']]; P['long_ctr'] += 1#; ctr += 1

				
				Data_moment = get_Data_moment(P,dm=dm,FLIP=FLIP)

				if Data_moment == False:
					continue

				ctr += 1

				if 'ctr' not in dm:
					dm['ctr'] = 0

				dm['ctr'] += 1
				dm['loss'] = []
				P['current_batch'].append(dm)
				D['names'].insert(0,Data_moment['name']) # This to match torch.cat use below
				D['flips'].insert(0,Data_moment['FLIP']) # This to match torch.cat use below


				list_camera_input = []
				for t in range(D['network']['net'].N_FRAMES):
					for camera in ('left', 'right'):
						list_camera_input.append(torch.from_numpy(Data_moment[camera][t]))
				camera_data = torch.cat(list_camera_input, 2)


				camera_data = camera_data.cuda().float()/255. - 0.5
				camera_data = torch.transpose(camera_data, 0, 2)
				camera_data = torch.transpose(camera_data, 1, 2)
				D['camera_data'] = torch.cat((torch.unsqueeze(camera_data, 0), D['camera_data']), 0)


				if type(P['metadata_constant_blanks']) == type(False):
					assert P['metadata_constant_blanks'] == False
					cr("************* making metadata_constant *************")

					mode_ctr = len(Data_moment['labels'])
					metadata_constant = torch.FloatTensor().cuda()
					num_metadata_channels = 128
					num_multival_metas = 1 + 4 + 12 + 3
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
					for camera in ('left', 'right'):
						for color in [0,1,2]: 
							img = cv2.resize(Data_moment[camera][t][:,:,color] ,(41,23))
							img0 = zeros((1,1,23,41))
							img0[0,0,:,:] = img
							img1 = torch.from_numpy(img0)
							img2 = img1.cuda().float()/255. - 0.5
							cat_list.append(img2)


				for j in range(3):
					img = D['zeros, metadata_size']
					img[0,0,:,:] = Data_moment['projections'][:,:,j]
					img = torch.from_numpy(img)
					img = img.cuda().float()/255.
					cat_list.append(img)
				

				cat_list.append(P['metadata_constant_blanks'])


				metadata_I = torch.cat(cat_list, 1)

				metadata = torch.FloatTensor().cuda()

				for cur_label in P['behavioral_modes']:

					if cur_label in Data_moment['labels']:


						if Data_moment['labels'][cur_label]:
							
							metadata = torch.cat((one_matrix, metadata), 1)
						else:
							metadata = torch.cat((zero_matrix, metadata), 1)
					else:
						metadata = torch.cat((zero_matrix, metadata), 1)

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
					
				#print metadata.size()

				D['metadata'] = torch.cat((metadata, D['metadata']), 0)






				if False:
					sv = Data_moment['steer']
					mv = Data_moment['motor']
					#rv = range(8,91,9)
					rv = P['prediction_range'] #range(10)
					sv = array(sv)[rv]
					mv = array(mv)[rv]
					steerv0 = torch.from_numpy(sv).cuda().float() / 99.
					motorv0 = torch.from_numpy(mv).cuda().float() / 99.
					steerv1 = (99-torch.from_numpy(sv).cuda().float()) / 99.
					motorv1 = (99-torch.from_numpy(mv).cuda().float()) / 99.
					target_datav = torch.unsqueeze(torch.cat((steerv0, motorv0,steerv1, motorv1), 0), 0)
					D['target_data'] = torch.cat((target_datav, D['target_data']), 0)



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
		True
		#Trial_loss_record = D['network'][data_moment_loss_record]
		D['network']['optimizer'].zero_grad()
		D['outputs'] = D['network']['net'](torch.autograd.Variable(D['camera_data']), torch.autograd.Variable(D['metadata'])).cuda()
		D['loss'] = D['network']['criterion'](D['outputs'], torch.autograd.Variable(D['target_data']))



	na = np.array
	def _function_backward():
		try:
			D['tries'] += 1
			D['loss'].backward()
			nnutils.clip_grad_norm(D['network']['net'].parameters(), 1.0)
			D['network']['optimizer'].step()

			if True: # np.mod(D['tries'],100) == 0:
				P['LOSS_LIST'].append(D['loss'].data.cpu().numpy()[:].mean())
				
				try:
					assert(len(P['current_batch']) == P['BATCH_SIZE'])
				except:
					print(len(P['current_batch']),P['BATCH_SIZE'])
				for i in range(P['BATCH_SIZE']):
					P['current_batch'][i]['loss'].append(P['LOSS_LIST'][-1])
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
			#D['tries'] = 0
			#D['successes'] = 0			

	Timer_updates = {
		'print_timer_time':'print_timer',
		'loss_timer_time':'loss_timer',
		'spause_timer_time':'spause_timer',
		'reload_image_file_timer_time':'reload_image_file_timer',
		'menu_load_timer_time':'menu_load_timer',
	}


	def _function_display():
		##################################
		#
		load_parameters(P,customer='train menu')

		for u in Timer_updates.keys():
			if u in P['updated']:
				P[Timer_updates[u]] = Timer(P[u])
				P['updated'].remove(u)
		#
		##################################
		#cv2.waitKey(1) # This is to keep cv2 windows alive
		if P['spause_timer'].check():
			spause()
			P['spause_timer'].reset()

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
	if P['DISPLAY_EACH']:
		D['DISPLAY'] = _function_display_each
	else:
		D['DISPLAY'] = _function_display
	return D






#EOF
