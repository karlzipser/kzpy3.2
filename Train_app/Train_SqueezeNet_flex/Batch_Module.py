from Parameters_Module import *
exec(identify_file_str)
from kzpy3.vis3 import *
import torch
import torch.nn.utils as nnutils
import Activity_Module
import kzpy3.Data_app.collect_flex_data2 as fx

Fd = fx.get_flex_data(fx.h5py_runs_folder)

P['long_ctr'] = -1
P['LOSS_LIST'] = []
if 'LOSS_LIST_AVG' not in P:
	P['LOSS_LIST_AVG'] = []


P['_flp'] = False
P['_indx'] = 1000



def Batch(the_network=None):
	D = {}
	D['successes'] = 0
	D['network'] = the_network
	True
	D['batch_size'] = P['BATCH_SIZE']
	D['camera_data'] = torch.FloatTensor().cuda()
	#D['metadata'] = torch.FloatTensor().cuda()
	D['target_data'] = torch.FloatTensor().cuda()
	#D['names'] = []
	#D['states'] = []
	D['tries'] = 0





	def _function_fill():
		#cs('a')
		ctr = 0
		#P['current_batch'] = []
		#cs('b')
		dimg = zeros((19,18,3))
		while ctr < D['batch_size']:

			#spause()#raw_enter()
			###Fs = fx.get_flex_segs(Fd,flip=P['_flp']),index=P['_indx'])
			Fs = fx.get_flex_segs(Fd,flip=random.choice([False,True]))
			if False:
				if P['_flp'] == False:
					P['_flp'] = True
				else:
					P['_indx'] += 10;print P['_indx']
					P['_flp'] = False

			if True:
				if np.random.rand(1)[0]<0.25:
					noise_level = 0
				else:
					noise_level = 5 * np.random.rand(1)[0]
				#noise_level = 0;cs('noise_level = 0')
				#print noise_level
			#noise_level = 0.33
			for q in Fs.keys():

				if 'F' == q[0]:
					Fs[q] *= max(0.1,(1.0+np.random.randn(1)[0]/5.0))
					Fs[q] += noise_level*25.0*np.random.randn(36)
					Fs[q] += noise_level*100.0*np.random.randn(1)
					#if noise_level == 0:
					#	Fs[q] *= 0 #TEMP!
			
			img = fx.make_flex_image(Fs) # STOPPED TEST: test, getting 18x3x3 image and 
			# reducing to 18x3x3 by randomly ignoring rows.
			"""
			index = 0
			indicies = []
			for i in range(18):
				indicies.append(index)
				index += random.choice([1,2])
			assert len(indicies) == 18
			assert max(indicies) < 36
			"""
			#img = img[indicies,:,:]
			"""
			dimg[fx.num_backward_timesteps,:,:]=2000
			dimg[fx.num_backward_timesteps,0,:]=-2000
			dimg[:fx.num_backward_timesteps,:,:] = img
			mi(z2o(dimg),'img');spause()			
			"""
			list_camera_input = []
			list_camera_input.append(torch.from_numpy(img))
			camera_data = torch.cat(list_camera_input, 2)
			camera_data = camera_data.cuda().float()/4000.0
			camera_data = torch.transpose(camera_data, 0, 2)
			camera_data = torch.transpose(camera_data, 1, 2)
			D['camera_data'] = torch.cat((torch.unsqueeze(camera_data, 0), D['camera_data']), 0)
			#cs('d')
			"""
			graphics = True
			if graphics:
				dimg = zeros((fx.num_backward_timesteps+1,3*fx.num_flex_locations,3))
				dimg[fx.num_backward_timesteps,:,:]=2000
				dimg[fx.num_backward_timesteps,0,:]=-2000
				dimg[:fx.num_backward_timesteps,:,:] = img.copy()
				mi(z2o(dimg),'img')
				figure('motor');clf()
				plot(49+0*Fs['steer'][fx.num_backward_timesteps:],'k-')
				plot(Fs['motor'][fx.num_backward_timesteps:],'b.-')
				plot(Fs['steer'][fx.num_backward_timesteps:],'r.-')
				ylim(0,99)
				spause()
				raw_enter()
			"""
			#cs('e')
			mv = Fs['motor'][fx.num_backward_timesteps:]
			sv = Fs['steer'][fx.num_backward_timesteps:]

			#rv = P['prediction_range'] #range(10)
			#sv = array(sv)[rv]
			#mv = array(mv)[rv]
			steerv = torch.from_numpy(sv).cuda().float() / 99.
			motorv = torch.from_numpy(mv).cuda().float() / 99.
			target_datav = torch.unsqueeze(torch.cat((steerv, motorv), 0), 0)
			D['target_data'] = torch.cat((target_datav, D['target_data']), 0)
			#cs('f')
			P['frequency_timer'].freq()
			#cs('freq')
			ctr+=1
		#cs('batch done')









	def _function_clear():
		#cs('clear')
		D['camera_data'] = torch.FloatTensor().cuda()
		D['metadata'] = torch.FloatTensor().cuda()
		D['target_data'] = torch.FloatTensor().cuda()
		D['states'] = []
		D['names'] = []
		D['outputs'] = None
		D['loss'] = None





	def _function_forward():
		#cs('forward')
		True
		D['network']['optimizer'].zero_grad()
		D['outputs'] = D['network']['net'](torch.autograd.Variable(D['camera_data'])).cuda()
		D['loss'] = D['network']['criterion'](D['outputs'], torch.autograd.Variable(D['target_data']))



	na = np.array
	def _function_backward():
		try:
			D['tries'] += 1
			D['loss'].backward()
			nnutils.clip_grad_norm(D['network']['net'].parameters(), 1.0)
			D['network']['optimizer'].step()

			P['LOSS_LIST'].append(D['loss'].data.cpu().numpy()[:].mean())
			
			#try:
			#	assert(len(P['current_batch']) == P['BATCH_SIZE'])
			#except:
			#	print('129',len(P['current_batch']),P['BATCH_SIZE'])
			#if True:
			#	for i in range(P['BATCH_SIZE']):
			#		P['current_batch'][i]['loss'].append(P['LOSS_LIST'][-1])
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
			#pd2s( D['tries'],D['successes'],int(100*D['successes']/(1.0*D['tries'])),"percent successes" )
	

	def _function_display():
		#cs('here')
		cv2.waitKey(1) # This is to keep cv2 windows alive
		if P['print_timer'].check():
			cg("Train_SqueezeNet_flex",P['start time'],'elapsed time =',intr(time.time()-P['start time numeric']))
			if False:#P['print_timer2'].check():
				figure('FC0')
				plot(Fd['FC0'][:])
				figure('steer')
				plot(Fd['steer'][:])
				figure('motor')
				plot(Fd['motor'][:])
				P['print_timer2'].reset()
			for i in [0]:#range(P['BATCH_SIZE']):
				ov = np.squeeze(D['outputs'][i].data.cpu().numpy())
				#mv = D['metadata'][i].cpu().numpy()
				tv = D['target_data'][i].cpu().numpy()
				#print 'len ov,tv',len(ov),len(tv)
				#raw_enter()
				#print('Loss:',dp(D['loss'].data.cpu().numpy()[0],5))
				av = D['camera_data'][i][:].cpu().numpy()
				#sbpd2s(shape(av))
				#bv = av.transpose(1,2,0)
				#srpd2s(shape(bv))
				#cv = z2o(bv)
				print(d2s(i,'camera_data min,max =',av.min(),av.max()))
				if P['loss_timer'].check() and len(P['LOSS_LIST_AVG'])>5:
					figure('LOSS_LIST_AVG '+P['start time'])
					clf()
					plot(P['LOSS_LIST_AVG'][int(0.25*len(P['LOSS_LIST_AVG'])):],'.')
					spause()
					P['loss_timer'].reset()
				Net_activity = Activity_Module.Net_Activity('batch_num',i, 'activiations',D['network']['net'].A)
				Net_activity['view']('moment_index',i,'delay',33, 'scales',{'camera_input':4,'pre_metadata_features':1,'post_metadata_features':2})
				#for a in D['network']['net'].A.keys():
				#	print shape(D['network']['net'].A[a])
				#bm = 'unknown behavioral_mode'
				#for j in range(len(P['behavioral_modes'])):
				#	if mv[-(j+1),0,0]:
				#		bm = P['behavioral_modes'][j]
				figure(d2s('steer',P['start time'],P['_flp']))
				clf()
				plt.title(d2s(i))
				ylim(-0.05,1.05);xlim(0,len(tv))
				plot([-1,20],[0.49,0.49],'k');
				plot([-1,20],[0.0,0.0],'k')
				#print ov,shape(ov)
				#print tv,shape(tv)
				plot(ov,'og')
				plot(tv,'or')
				spause()
				P['print_timer'].reset()




	D['FILL'] = _function_fill
	D['CLEAR'] = _function_clear
	D['FORWARD'] = _function_forward
	D['BACKWARD'] = _function_backward
	D['DISPLAY'] = _function_display




	return D






#EOF
