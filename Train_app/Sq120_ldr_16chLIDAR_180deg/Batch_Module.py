from kzpy3.vis3 import *
import Data_Module
import torch
import torch.nn.utils as nnutils
import Activity_Module
exec(identify_file_str)

LIDAR_WIDTH = 690/2
LIDAR_HEIGHT = 64




Translation = {
	'steer':'steer',
	'motor':'motor',
	'gyro_heading_x':'heading',
	'encoder_meo':'encoder',
}

def Batch(_,the_network=None,the_network_depth=None):

	if _['start menu automatically'] and using_linux():
	    dic_name = "_"
	    sys_str = d2n("gnome-terminal  --geometry 40x30+100+200 -x python kzpy3/Menu_app/menu2.py path ",project_path," dic ",dic_name)
	    cr(sys_str)
	    os.system(sys_str)

	D = {}
	D['network'] = the_network
	D['batch_size'] = _['BATCH_SIZE']
	D['camera_data'] = torch.FloatTensor().cuda()
	D['metadata'] = torch.FloatTensor().cuda()
	D['target_data'] = torch.FloatTensor().cuda()
	D['names'] = []
	D['flips'] = []
	D['states'] = []
	D['tries'] = 0
	D['successes'] = 0
	D['zeros, metadata_size'] = zeros((1,1,23,41))

	_['data_moments_indexed_loaded'] = []
	_['metadata_constant_blanks'] = False
	_['metadata_constant_gradients'] = False
	_['long_ctr'] = -1
	_['LOSS_LIST'] = []
	if 'LOSS_LIST_AVG' not in _:
		_['LOSS_LIST_AVG'] = []
	_['reload_image_file_timer'].trigger()
	_['ZED_image'] = None

	Data_Module.prepare_data_for_training(_)
	Network_Predictions = Data_Module.load_Network_Predictions(_)

	zero_matrix = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()
	one_matrix = torch.FloatTensor(1, 1, 23, 41).fill_(1).cuda()
	temp = (255*z2o(np.random.randn(94,168))).astype(np.uint8)
	zero_94_168_img = zeros((94,168),np.uint8)


	D['network_depth'] = the_network_depth
	D['camera_data_depth'] = torch.FloatTensor().cuda()
	D['metadata_depth'] = torch.FloatTensor().cuda()
	D['zeros, metadata_size_depth'] = zeros((1,1,15,86))
	_['metadata_constant_blanks_depth'] = False
	_['metadata_constant_gradients_depth'] = False
	zero_matrix_depth = torch.FloatTensor(1, 1, 15, 86).zero_().cuda()
	one_matrix_depth = torch.FloatTensor(1, 1, 15, 86).fill_(1).cuda()
	temp_depth = (255*z2o(np.random.randn(LIDAR_HEIGHT,LIDAR_WIDTH))).astype(np.uint8)
	zero_94_168_img_depth = zeros((LIDAR_HEIGHT,LIDAR_WIDTH),np.uint8)





	def _load_image_files():
		cy('_load_image_files()')
		_['Loaded_image_files'] = {}

		shuffled_keys = _['run_name_to_run_path'].keys()
		random.shuffle(shuffled_keys)


		for f in shuffled_keys[:_['max_num_runs_to_open']]:

			cg('_load_image_files():',f)
			_['Loaded_image_files'][f] = {}
			if True:
				try:

					L,O,F = open_run(run_name=f,h5py_path=pname(_['run_name_to_run_path'][f]))

					_['Loaded_image_files'][f]['normal'] = O
					_['Loaded_image_files'][f]['flip'] = F
					_['Loaded_image_files'][f]['left_timestamp_metadata'] = L

					if _['use_LIDAR']:
						path = opj(_['LIDAR_path'],f+_['LIDAR_extension'])
						cg("*",path,"*")
						#raw_enter()
						R = h5r(path)
						_['Loaded_image_files'][f]['depth'] = R
						#cg("*",path," success*")
						#raw_enter()


					#print f
				except Exception as e:
					print("********** Exception ***********************")
					print(e.message, e.args)

		if _['verbose']: print(len(_['Loaded_image_files']))

		pd2s('1) len(_[data_moments_indexed]) =',len(_['data_moments_indexed']))

		timer = Timer()
		_['data_moments_indexed_loaded'] = []



		if "ORIGINAL VERSION":
			for dm in _['data_moments_indexed']:
				if dm['run_name'] in _['Loaded_image_files']:
					_['data_moments_indexed_loaded'].append(dm)
		else: 
			for dm in _['data_moments_indexed']:
				if dm['run_name'] in _['Loaded_image_files']:
					if np.random.random() < 0.1:
						cg('yes')
						_['data_moments_indexed_loaded'].append(dm)
					else:
						cr('no')



		random.shuffle(_['data_moments_indexed_loaded'])

		pd2s('index discovery time =',timer.time(),'len(_[data_moments_indexed_loaded]) =',len(_['data_moments_indexed_loaded']))
	






	def _close_image_files():

		cy('_close_image_files()')

		for f in _['Loaded_image_files']:

			try:
				_['Loaded_image_files'][f]['normal'].close()
				_['Loaded_image_files'][f]['flip'].close()


				_['Loaded_image_files'][f]['left_timestamp_metadata'].close()
				if _['use_LIDAR']:
					_['Loaded_image_files'][f]['depth'].close()

			except Exception as e:
				print("********** _close_image_files Exception ***********************")
				print(e.message, e.args)







	def _function_fill():

		if _['reload_image_file_timer'].check():
			_close_image_files()
			_load_image_files()
			_['reload_image_file_timer'].reset()

		ctr = 0
		_['current_batch'] = []
		while ctr < D['batch_size']:
			if True:#try:
				if _['long_ctr'] == -1 or _['long_ctr'] >= len(_['data_moments_indexed_loaded']):
					_['long_ctr'] = 0
					random.shuffle(_['data_moments_indexed_loaded'])
					cy('random.shuffle(_[data_moments_indexed_loaded])')
				
				FLIP = random.choice([0,1])
				#cr(len(_['data_moments_indexed_loaded']),_['long_ctr'])
				dm = _['data_moments_indexed_loaded'][_['long_ctr']]; _['long_ctr'] += 1#; ctr += 1

				
				Data_moment = Data_Module.get_Data_moment(_,Network_Predictions,dm=dm,FLIP=FLIP)

				if Data_moment == False:
					continue

				ctr += 1

				if 'ctr' not in dm:
					dm['ctr'] = 0

				dm['ctr'] += 1
				dm['loss'] = []
				_['current_batch'].append(dm)
				D['names'].insert(0,Data_moment['name']) # This to match torch.cat use below
				D['flips'].insert(0,Data_moment['FLIP']) # This to match torch.cat use below














				###################################################################
				###################################################################
				###################################################################
				####	METADATA depth

				if type(_['metadata_constant_blanks_depth']) == type(False):
					assert _['metadata_constant_blanks_depth'] == False
					cr("************* making metadata_constant_depth *************")

					mode_ctr = len(Data_moment['labels'])
					metadata_constant_depth = torch.FloatTensor().cuda()
					num_metadata_channels = 128
					num_multival_metas = 1 + 4 + 12 + 3#+ 27
					for i in range(num_metadata_channels - num_multival_metas - mode_ctr): # Concatenate zero matrices to fit the dataset
						metadata_constant_depth = torch.cat((zero_matrix_depth, metadata_constant_depth), 1)
					_['metadata_constant_blanks_depth'] = metadata_constant_depth

					metadata_constant_depth = torch.FloatTensor().cuda()
					meta_gradient1 = zero_matrix_depth.clone()
					for x in range(15):
						meta_gradient1[:,:,x,:] = x/15.0#torch.from_numpy(rnd[:,:,:,y])
					metadata_constant_depth = torch.cat((meta_gradient1, metadata_constant_depth), 1) #torch.from_numpy(meta_a)

					meta_gradient2 = zero_matrix_depth.clone()
					for x in range(15):
						meta_gradient2[:,:,x,:] = (1.0-x/15.0)#torch.from_numpy(rnd[:,:,:,y])
					metadata_constant_depth = torch.cat((meta_gradient2, metadata_constant_depth), 1) #torch.from_numpy(meta_a)

					meta_gradient3 = zero_matrix_depth.clone()
					for x in range(86):
						meta_gradient3[:,:,:,x] = x/86.0#torch.from_numpy(rnd[:,:,:,y])
					metadata_constant_depth = torch.cat((meta_gradient3, metadata_constant_depth), 1) #torch.from_numpy(meta_a)

					meta_gradient4 = zero_matrix_depth.clone()
					for x in range(86):
						meta_gradient4[:,:,:,x] = (1.0-x/86.0)#torch.from_numpy(rnd[:,:,:,y])
					metadata_constant_depth = torch.cat((meta_gradient4, metadata_constant_depth), 1) #torch.from_numpy(meta_a)
					_['metadata_constant_gradients_depth'] = metadata_constant_depth



				cat_list_depth = [_['metadata_constant_gradients_depth']]

				for t in range(2):#D['network']['net'].N_FRAMES):
					for camera in ('left', 'right'):
						for color in [0,2,1]:
							if True:
								#img = cv2.resize(Data_moment[camera][t][:,:,color] ,(86,15))
								img0 = zeros((1,1,15,86))
								#img0[0,0,:,:] = img
								img1 = torch.from_numpy(img0)
								img2 = img1.cuda().float()#/255. - 0.5
								cat_list_depth.append(img2)
							else:
								cat_list_depth.append(zero_matrix_depth)

				################################################################
				# projection metadata (just zeros)
				if True:
					for j in [0,2,1]:
						img = D['zeros, metadata_size_depth']
						#img[0,0,:,:] = zero_matrix_depth.clone()#cv2.resize(Data_moment['projections'][:,:,j] ,(86,15))
						img = torch.from_numpy(img)
						img = img.cuda().float()/255.
						cat_list_depth.append(img)
				#
				################################################################
				

				cat_list_depth.append(_['metadata_constant_blanks_depth'])

				#for c in cat_list_depth:
				#	cb(c.size())

				metadata_I_depth = torch.cat(cat_list_depth, 1)

				metadata_depth = torch.FloatTensor().cuda()

				for cur_label in _['behavioral_modes']:

					if cur_label in Data_moment['labels']:

						if False:
							
							metadata_depth = torch.cat((one_matrix_depth, metadata_depth), 1);#mode_ctr += 1
						else:
							metadata_depth = torch.cat((zero_matrix_depth, metadata_depth), 1);#mode_ctr += 1
					else:
						metadata_depth = torch.cat((zero_matrix_depth, metadata_depth), 1);#mode_ctr += 1


				metadata_depth = torch.cat((metadata_I_depth, metadata_depth), 1)


				for topic in ['encoder']:
					meta_gradient5 = zero_matrix_depth.clone()
					d = Data_moment[topic+'_past']/100.0
					if topic == 'encoder':
						med = np.median(d)
						for i in range(len(d)):
							if d[i] < med/3.0:
								d[i] = med # this to attempt to get rid of drop out from magnet not being read
						d = d/5.0
					d = d.reshape(-1,3).mean(axis=1)
					for x in range(0,15):
						meta_gradient5[:,:,x,:] = d[x]
					metadata_depth = torch.cat((meta_gradient5, metadata_depth), 1)
					

				D['metadata_depth'] = torch.cat((metadata_depth, D['metadata_depth']), 0)
				####
				###################################################################
				###################################################################
				###################################################################


















				if False:
					###################################################################
					###################################################################
					###################################################################
					#### CAMERA DATA

					#zeroed_channels = np.random.choice([ [0],[2],[0,2],[0,2],[0,2], ])
					zeroed_channels = []

					list_camera_input = []
					for t in range(D['network']['net'].N_FRAMES):
						for camera in ('left', 'right'):
							img = Data_moment[camera][t]
							for c in zeroed_channels:
								img[:,:,c] = zero_94_168_img
							list_camera_input.append(torch.from_numpy(img))
					camera_data = torch.cat(list_camera_input, 2)



					camera_data = camera_data.cuda().float()/255. - 0.5
					camera_data = torch.transpose(camera_data, 0, 2)
					camera_data = torch.transpose(camera_data, 1, 2)
					D['camera_data'] = torch.cat((torch.unsqueeze(camera_data, 0), D['camera_data']), 0)
					#####
					###################################################################
					###################################################################
					###################################################################

				if ctr == D['batch_size']:#0+1: # ctr has already been incremented by this point
					_['ZED_image'] = Data_moment['left'][0]
					#cg( shape(_['ZED_image']), ra=1 )



				###################################################################
				###################################################################
				###################################################################
				#### CAMERA DATA depth

				#zeroed_channels = np.random.choice([ [0],[2],[0,2],[0,2],[0,2], ])

				field_of_view_deg = 360#int(270 + 15*randn())
				if field_of_view_deg > 360:
					field_of_view_deg = 360
				if field_of_view_deg <180:
					field_of_view_deg = 180
				pixel_field_offset = int(LIDAR_WIDTH/360.*(360-field_of_view_deg)/2.)

				list_camera_input_depth = []

				for t in ['depth_image_0','depth_image_n1']:
					img = Data_moment[t][:,690/4:-690/4,:]
					#img[:,:pixel_field_offset,:] = 127
					#img[:,-pixel_field_offset:,:] = 127
					img[:,:,2] = 0
					list_camera_input_depth.append(torch.from_numpy(img))
				camera_data_depth = torch.cat(list_camera_input_depth, 2)



				camera_data_depth = camera_data_depth.cuda().float()/255. - 0.5
				camera_data_depth = torch.transpose(camera_data_depth, 0, 2)
				camera_data_depth = torch.transpose(camera_data_depth, 1, 2)
				D['camera_data_depth'] = torch.cat((torch.unsqueeze(camera_data_depth, 0), D['camera_data_depth']), 0)
				#####
				###################################################################
				###################################################################
				###################################################################








				###################################################################
				###################################################################
				###################################################################
				#### TARGET DATA




				sv = Data_moment['steer']
				mv = Data_moment['motor']
				hv = Data_moment['gyro_heading_x']
				ev = Data_moment['encoder_meo']

				rv = _['prediction_range']

				sv = array(sv)[rv]
				mv = array(mv)[rv]
				hv = array(hv)[rv]
				ev = array(ev)[rv]

				
				Data_moment['steer'] = sv
				Data_moment['motor'] = mv
				Data_moment['gyro_heading_x'] = hv
				Data_moment['encoder_meo'] = ev		


				for s in ['left','direct','right']:
					if Data_moment['labels'][s]:#True:#False:#Data_moment['labels'][s]:
						for m in ['steer','motor','gyro_heading_x','encoder_meo']:
							n = Translation[m]
							Data_moment['predictions'][s][n] = Data_moment[m]
						break




				modified = False
				# because the first prediction can sometimes be extremely low,
				for u in [0,1]:
					if Data_moment['predictions']['direct']['motor'][u] <= 49:
						Data_moment['predictions']['direct']['motor'][u] = max(Data_moment['predictions']['direct']['motor'][:3])#,Data_moment['predictions']['direct']['motor'][1])
						if False and ctr == D['batch_size'] and u == 1:
							figure(1);clf();plot(Data_moment['predictions']['direct']['motor'],'.-')
							spause();raw_enter()
					if Data_moment['predictions']['direct']['encoder'][u] <= 0.1:
						Data_moment['predictions']['direct']['encoder'][u] = max(Data_moment['predictions']['direct']['encoder'][:3])#,Data_moment['predictions']['direct']['encoder'][1])
						if False and ctr == D['batch_size'] and u == 1:
							figure(2);clf();plot(Data_moment['predictions']['direct']['encoder'],'.-')
							spause();raw_enter()
				for i in rlen(Data_moment['predictions']['direct']['motor']):
					if Data_moment['predictions']['direct']['motor'][i] <= 49 or Data_moment['predictions']['direct']['encoder'][i] <= 0.1:
						for s in ['left','right']:
							for em in ['motor','encoder']:
								Data_moment['predictions'][s][em][i] = Data_moment['predictions']['direct'][em][i]
						modified = True
				"""
				for i in rlen(Data_moment['predictions']['direct']['motor']):
					if Data_moment['predictions']['direct']['motor'][i] < 49 or Data_moment['predictions']['direct']['encoder'][i] < 0.1:
						for s in ['left','right']:
							for em in ['motor','encoder']:
								Data_moment['predictions'][s][em][i] = Data_moment['predictions']['direct'][em][i]
						modified = True
				"""




				if False and modified:
					figure(6);clf();plt.title(time_str())
					for s in ['left','direct','right']:
						plot(Data_moment['predictions'][s]['motor'],'.-')
					figure(7);clf()
					for s in ['left','direct','right']:
						plot(Data_moment['predictions'][s]['encoder'],'.-')
					spause()
					raw_enter()




					#else:
					#	for m in ['steer','motor','gyro_heading_x','encoder_meo']:
					#		n = Translation[m]
					#		Data_moment['predictions'][s][n] = Data_moment[m]*0						

				sv = np.concatenate((
					Data_moment['predictions']['left']['steer'],
					Data_moment['predictions']['direct']['steer'],
					Data_moment['predictions']['right']['steer']),0)
				mv = np.concatenate((
					Data_moment['predictions']['left']['motor'],
					Data_moment['predictions']['direct']['motor'],
					Data_moment['predictions']['right']['motor']),0)
				hv = np.concatenate((
					Data_moment['predictions']['left']['heading']-Data_moment['predictions']['left']['heading'][0],
					Data_moment['predictions']['direct']['heading']-Data_moment['predictions']['direct']['heading'][0],
					Data_moment['predictions']['right']['heading']-Data_moment['predictions']['right']['heading'][0]),0)
				ev = np.concatenate((
					Data_moment['predictions']['left']['encoder'],
					Data_moment['predictions']['direct']['encoder'],
					Data_moment['predictions']['right']['encoder']),0)
				

				for q in rlen(mv):
					if mv[q] < 49:
						ev[q] *= -1

				if False:
					hv = hv - hv[0]

				steer = sv / 99.
				motor = mv / 99.
				heading = hv / 90.0
				encoder = ev / 5.0

				steer_c = torch.from_numpy(steer).cuda().float()
				motor_c = torch.from_numpy(motor).cuda().float()
				heading_c = torch.from_numpy(heading).cuda().float()
				encoder_c = torch.from_numpy(encoder).cuda().float()

				if False:#
					concat = np.concatenate((steer,motor,heading,encoder), axis=0)
					target_data_depth = zeros((1,120))
					for i in range(1):
						target_data_depth[0,:] = concat
					D['target_data_depth'] = torch.from_numpy(target_data_depth).cuda().float()

				#target_data = torch.unsqueeze(torch.cat((
				#	steer,steer,steer,motor,motor,motor,heading,heading,heading,encoder,encoder,encoder), 0), 0)
				
				target_data = torch.unsqueeze(torch.cat((steer_c,motor_c,heading_c,encoder_c), 0), 0)

				D['target_data'] = torch.cat((target_data, D['target_data']), 0)
				#raw_enter(d2s('target_data',target_data.size()))
				#raw_enter(d2s('target_data_depth',D['target_data_depth'].size()))
				#cy(D['target_data'],ra=1)
				####
				###################################################################
				###################################################################
				###################################################################


				if False:
					print 'Batch_Module graphics'
					#mci(Data_moment['left'][0],title='left',scale=3.0)
					figure(1);clf()
					plot(-(Data_moment['predictions']['left']['heading']-Data_moment['predictions']['left']['heading'][0]),range(10),'r.-')
					plot(-(Data_moment['predictions']['direct']['heading']-Data_moment['predictions']['direct']['heading'][0]),range(10),'b.-')
					plot(-(Data_moment['predictions']['right']['heading']-Data_moment['predictions']['right']['heading'][0]),range(10),'g.-')
					plt.title(d2s('FLIP ==',FLIP))
					xylim(-45,45,0,10);spause()
					raw_enter()




				_['frequency_timer'].freq(
					cf(
						host_name,'`b-d',
						'train duration =','`',
						int(_['duration timer'].time()/60),
						"minutes",'`y-b',
						time_str('TimeShort'),'`-b',
					)
				)
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

		D['camera_data_depth'] = torch.FloatTensor().cuda()
		D['metadata_depth'] = torch.FloatTensor().cuda()
		#D['target_data'] = torch.FloatTensor().cuda()
		#D['states'] = []
		#D['names'] = []
		D['outputs_depth'] = None
		D['loss_depth'] = None




	def _function_forward():
		True
		#Trial_loss_record = D['network'][data_moment_loss_record]
		if False:
			D['network']['optimizer'].zero_grad()
			D['outputs'] = D['network']['net'](torch.autograd.Variable(D['camera_data']), torch.autograd.Variable(D['metadata'])).cuda()
			D['loss'] = D['network']['criterion'](D['outputs'], torch.autograd.Variable(D['target_data']))
		#raw_enter(d2s('target_data',D['target_data'].size()))
		#raw_enter(d2s('outputs',D['outputs'].size()))


		D['network_depth']['optimizer'].zero_grad()
		#raw_enter(d2s('camera_data_depth',D['camera_data_depth'].size()))
		#raw_enter(d2s('metadata_depth',D['metadata_depth'].size()))
		#raw_enter(d2s('target_data',D['target_data'].size()))
		#raw_enter(d2s('outputs',D['outputs'].size()))
		D['outputs_depth'] = D['network_depth']['net'](torch.autograd.Variable(D['camera_data_depth']), torch.autograd.Variable(D['metadata_depth'])).cuda()
		#raw_enter(d2s('target_data_depth',D['target_data_depth'].size()))
		#raw_enter(d2s('outputs_depth',D['outputs_depth'].size()))
		D['loss_depth'] = D['network_depth']['criterion'](D['outputs_depth'], torch.autograd.Variable(D['target_data']))


	na = np.array
	def _function_backward():
		if True:#try:
			D['tries'] += 1

			if False:
				D['loss'].backward()
				nnutils.clip_grad_norm(D['network']['net'].parameters(), 1.0)
				D['network']['optimizer'].step()


			D['loss_depth'].backward()
			nnutils.clip_grad_norm(D['network_depth']['net'].parameters(), 1.0)
			#raw_enter(d2s('network_depth in D','network_depth' in D))
			#raw_enter(d2s('D[network_depth][optimizer] in D','optimizer' in D['network_depth']))
			D['network_depth']['optimizer'].step()


			if True: # np.mod(D['tries'],100) == 0:
				if False:
					_['LOSS_LIST'].append(D['loss'].data.cpu().numpy()[:].mean())
				else:
					try:
						_['LOSS_LIST'].append(D['loss_depth'].data.cpu().numpy()[:].mean())
					except:
						_['LOSS_LIST'].append(D['loss_depth'].data.cpu().numpy())
				
				try:
					assert(len(_['current_batch']) == _['BATCH_SIZE'])
				except:
					print(len(_['current_batch']),_['BATCH_SIZE'])
				for i in range(_['BATCH_SIZE']):
					_['current_batch'][i]['loss'].append(_['LOSS_LIST'][-1])
				if len(_['LOSS_LIST']) > _['LOSS_LIST_N']:
					_['LOSS_LIST_AVG'].append(na(_['LOSS_LIST']).mean())
					_['LOSS_LIST'] = []
			D['successes'] += 1

		else:#except Exception as e:
			print("********** Exception ****** def _function_backward(): failed!!!! *****************")
			print(e.message, e.args)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			CS_('Exception!',exception=True,newline=False)
			CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
			pd2s( D['tries'],D['successes'],int(100*D['successes']/(1.0*D['tries'])),"percent successes" )
			#D['tries'] = 0
			#D['successes'] = 0			




	def _function_display(network='network_depth'):
		
		if 'display on' not in _:
			_['display on'] = False
		if _['display']:
			_['display on'] = True
		if not _['display']:
			if _['display on']:
				CA()
				_['display on'] = False
			return
		if network == 'network_depth':
			suf = '_depth'
		else:
			suf = ''

		if _['spause_timer'].check():
			spause()
			_['spause_timer'].reset()

		if _['print_timer'].check():
			kprint(_['data_moment_count'],'data_moment_count',numbering=True)
			mi(_['ZED_image'],'ZED_image')
			cprint(d2s("_['start time'] =",_['start time']),'blue','on_yellow')
			for i in [0]:#range(_['BATCH_SIZE']):
				ov = D['outputs'+suf][i].data.cpu().numpy()
				mv = D['metadata'+suf][i].cpu().numpy()
				tv = D['target_data'][i].cpu().numpy()
				cg("len(ov),len(tv) =", len(ov),len(tv))
				#raw_enter()
				if _['verbose']: print('Loss:',dp(D['loss'].data.cpu().numpy()[0],5))
				av = D['camera_data'+suf][i][:].cpu().numpy()
				bv = av.transpose(1,2,0)
				hv = shape(av)[1]
				wv = shape(av)[2]

				if _['verbose']: print(d2s(i,'camera_data min,max =',av.min(),av.max()))
				
				Net_activity = Activity_Module.Net_Activity('P',_,'batch_num',i, 'activiations',D[network]['net'].A)
				Net_activity['view']('moment_index',i,'delay',33, 'scales',{'camera_input':1,'pre_metadata_features':0,'pre_metadata_features_metadata':0,'post_metadata_features':0})
				bm = 'unknown behavioral_mode'
				for j in range(len(_['behavioral_modes'])):
					if mv[-(j+1),0,0]:
						bm = _['behavioral_modes'][j]
					#else:
					#	cr(_['behavioral_modes'][j],'unknown behavioral_mode !!!')
				figure(fname(_['project_path'])+' steer '+_['start time'],figsize=_['figure size'])
				clf()
				plt.title(d2s(i))
				ylim(-1.05,1.05);xlim(0,len(tv))
				plot([-1,60],[0.49,0.49],'k');
				plot([-1,120],[0.0,0.0],'k')
				plot([30,30],[-1.0,1.0],'k:')
				plot([60,60],[-1.0,1.0],'k:')
				plot([90,90],[-1.0,1.0],'k:')
				#plot(ov,'o-g'); plot(tv,'o-r'); plt.title(D['names'][0])



				for u in range(12):
					v = 10*u
					plot(range(v,v+10),ov[v:v+10],'o-g')
					plot(range(v,v+10),tv[v:v+10],'o-r')

				#plot(tv,'o-r')


				plt.title(D['names'][0])



				#print(tv)
				if D['flips'][0]:
					flip_str = '(flip)'
				else:
					flip_str = ''
				plt.xlabel(d2s(bm,flip_str))
				if False:
					figure('metadata '+_['start time']);clf()
					plot(mv[-10:,0,0],'r.-')
					plt.title(d2s(bm,i))
				spause()
				_['print_timer'].reset()
			dm_ctrs_max = 100
			dm_ctrs = zeros(dm_ctrs_max)
			loss_list = []
			for j in range(len(_['data_moments_indexed'])):
				if 'ctr' in _['data_moments_indexed'][j]:
					k = _['data_moments_indexed'][j]['ctr']
					if k < dm_ctrs_max:
						dm_ctrs[k] += 1
				else:
					dm_ctrs[0] += 1
				if 'loss' in _['data_moments_indexed'][j]:
					if len(_['data_moments_indexed'][j]['loss']) > 0:
						loss_list.append(_['data_moments_indexed'][j]['loss'][-1])
			if False:
				figure('dm_ctrs '+_['start time'],figsize=(1,6));clf();plot(dm_ctrs,'.-');xlim(0,100)
			_['dm_ctrs'] = dm_ctrs
			#figure('loss_list');clf();hist(loss_list)
			spause()

			if bm == 'unknown behavioral_mode':
				cr('***','unknown behavioral_mode:',bm)
				#raw_enter()

		if _['loss_timer'].check() and len(_['LOSS_LIST_AVG'])>0:
			if _['num loss_list_avg steps to show'] == None:
				q = int(len(_['LOSS_LIST_AVG'])*_['percent_of_loss_list_avg_to_show']/100.0)
			else:
				q = min(_['num loss_list_avg steps to show'],len(_['LOSS_LIST_AVG']))
			figure(fname(_['project_path'])+' LOSS_LIST_AVG '+_['start time'],figsize=_['loss figure size'])
			clf()
			try:
				for loss_ in _['comparison losses']+[_['LOSS_LIST_AVG']]:
					plot(loss_[-q:],'.')
			except Exception as e:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				CS_('Exception!',emphasis=True)
				CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
			u = min(len(_['LOSS_LIST_AVG']),_['NUM_LOSS_STEPS_TO_AVERAGE']) # was 250
			median_val = np.median(na(_['LOSS_LIST_AVG'][-u:]))
			plt.title(d2s('1000*median =',dp(1000.0*median_val,3)))
			plot([0,q],[median_val,median_val],'r')
			plt.xlim(0,q);plt.ylim(0,0.05)
			spause()
			_['loss_timer'].reset()



	D['FILL'] = _function_fill
	D['CLEAR'] = _function_clear
	D['FORWARD'] = _function_forward
	D['BACKWARD'] = _function_backward
	if _['DISPLAY_EACH']:
		D['DISPLAY'] = _function_display_each
	else:
		D['DISPLAY'] = _function_display
	return D






#EOF
