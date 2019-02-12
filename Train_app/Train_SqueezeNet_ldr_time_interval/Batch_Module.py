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
	D['target_data'] = torch.FloatTensor().cuda()
	D['tries'] = 0





	def _function_fill():
		ctr = 0
		dimg = zeros((19,18,3))

		while ctr < D['batch_size']:

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

			for q in Fs.keys():

				if 'F' == q[0]:
					Fs[q] *= max(0.1,(1.0+np.random.randn(1)[0]/5.0))
					Fs[q] += noise_level*25.0*np.random.randn(36)
					Fs[q] += noise_level*100.0*np.random.randn(1)
			
			img = fx.make_flex_image(Fs) # STOPPED TEST: test, getting 18x3x3 image and 
			# reducing to 18x3x3 by randomly ignoring rows.

			list_camera_input = []
			list_camera_input.append(torch.from_numpy(img))
			camera_data = torch.cat(list_camera_input, 2)
			camera_data = camera_data.cuda().float()/4000.0
			camera_data = torch.transpose(camera_data, 0, 2)
			camera_data = torch.transpose(camera_data, 1, 2)
			D['camera_data'] = torch.cat((torch.unsqueeze(camera_data, 0), D['camera_data']), 0)

			mv = Fs['motor'][fx.num_backward_timesteps:]
			sv = Fs['steer'][fx.num_backward_timesteps:]

			steerv = torch.from_numpy(sv).cuda().float() / 99.
			motorv = torch.from_numpy(mv).cuda().float() / 99.
			target_datav = torch.unsqueeze(torch.cat((steerv, motorv), 0), 0)
			D['target_data'] = torch.cat((target_datav, D['target_data']), 0)
			P['frequency_timer'].freq()
			ctr+=1




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
	

	def _function_display():
		cv2.waitKey(1) # This is to keep cv2 windows alive
		if P['print_timer'].check():
			cg("Train_SqueezeNet_flex",P['start time'],'elapsed time =',intr(time.time()-P['start time numeric']))

			for i in [0]:#range(P['BATCH_SIZE']):
				ov = np.squeeze(D['outputs'][i].data.cpu().numpy())
				tv = D['target_data'][i].cpu().numpy()
				av = D['camera_data'][i][:].cpu().numpy()
				print(d2s(i,'camera_data min,max =',av.min(),av.max()))
				if P['loss_timer'].check() and len(P['LOSS_LIST_AVG'])>5:
					figure('LOSS_LIST_AVG '+P['start time'])
					clf()
					plot(P['LOSS_LIST_AVG'][int(0.25*len(P['LOSS_LIST_AVG'])):],'.')
					spause()
					P['loss_timer'].reset()
				Net_activity = Activity_Module.Net_Activity('batch_num',i, 'activiations',D['network']['net'].A)
				Net_activity['view']('moment_index',i,'delay',33, 'scales',{'camera_input':4,'pre_metadata_features':1,'post_metadata_features':2})

				figure(d2s('steer',P['start time'],P['_flp']))
				clf()
				plt.title(d2s(i))
				ylim(-0.05,1.05);xlim(0,len(tv))
				plot([-1,20],[0.49,0.49],'k');
				plot([-1,20],[0.0,0.0],'k')

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
