from kzpy3.vis3 import *
import Data_Module
import torch
import torch.nn.utils as nnutils
import Activity_Module
from ConDecon_Fire_get_data import make_batch
exec(identify_file_str)



def data_to_torch(Data):

    Torch_data = {}

    for k in Data:

        if type(Data[k]) != type(None):
            Torch_data[k] = torch.from_numpy(Data[k]).cuda(device=0).float()
        else:
            Torch_data[k] = None

    return Torch_data



Translation = {
	'steer':'steer',
	'motor':'motor',
	'gyro_heading_x':'heading',
	'encoder_meo':'encoder',
}

def Batch(_,the_network=None):

	if _['start menu automatically'] and using_linux():
	    dic_name = "_"
	    sys_str = d2n("gnome-terminal  --geometry 40x30+100+200 -x python kzpy3/Menu_app/menu2.py path ",project_path," dic ",dic_name)
	    cr(sys_str)
	    os.system(sys_str)

	D = {}
	D['network'] = the_network
	D['batch_size'] = _['BATCH_SIZE']
	D['camera_data'] = torch.FloatTensor().cuda()
	#D['metadata'] = torch.FloatTensor()#.cuda()
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





	def _function_fill():

		Data = make_batch(_['BATCH_SIZE'])
		Torch_data = data_to_torch(Data)

		if False:
			a = rnd((_['BATCH_SIZE'], 3, 47, 84))
			b = 0.01*rndn(_['BATCH_SIZE'], 3, 47, 84)
			D['camera_data'] = torch.from_numpy(a+b).float()
			D['target_data'] = torch.from_numpy(a).float()

		if False:
			print shape(Data['input'])
			print shape(Data['target'])
			print 

		D['camera_data'] = Torch_data['input'].float()
		D['target_data'] = Torch_data['target'].float()




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
		D['network']['optimizer'].zero_grad()
		D['outputs'] = D['network']['net'](torch.autograd.Variable(D['camera_data'])).cuda()
		D['loss'] = D['network']['criterion'](D['outputs'], torch.autograd.Variable(D['target_data']))




	def _function_backward():
		try:
			D['tries'] += 1
			D['loss'].backward()
			nnutils.clip_grad_norm(D['network']['net'].parameters(), 1.0)
			D['network']['optimizer'].step()

			if True: # np.mod(D['tries'],100) == 0:
				_['LOSS_LIST'].append(D['loss'].data.cpu().numpy()[:].mean())
				if len(_['LOSS_LIST']) > _['LOSS_LIST_N']:
					_['LOSS_LIST_AVG'].append(na(_['LOSS_LIST']).mean())
					_['LOSS_LIST'] = []
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

		if 'display on' not in _:
			_['display on'] = False
		if _['display']:
			_['display on'] = True
		if not _['display']:
			if _['display on']:
				CA()
				_['display on'] = False
			return

		if _['spause_timer'].check():
			spause()
			_['spause_timer'].reset()

		if False:#_['print_timer'].check():
			cprint(d2s("_['start time'] =",_['start time']),'blue','on_yellow')
			for i in [0]:#range(_['BATCH_SIZE']):
				ov = D['outputs'][i].data.cpu().numpy()
				#mv = D['metadata'][i].cpu().numpy()
				tv = D['target_data'][i].cpu().numpy()
				cg("len(ov),len(tv) =", len(ov),len(tv))
				#raw_enter()
				if _['verbose']: print('Loss:',dp(D['loss'].data.cpu().numpy()[0],5))
				av = D['camera_data'][i][:].cpu().numpy()
				bv = av.transpose(1,2,0)
				hv = shape(av)[1]
				wv = shape(av)[2]

				if _['verbose']: print(d2s(i,'camera_data min,max =',av.min(),av.max()))
				
				#Net_activity = Activity_Module.Net_Activity('P',_,'batch_num',i, 'activiations',D['network']['net'].A)
				#Net_activity['view']('moment_index',i,'delay',33, 'scales',{'camera_input':1,'pre_metadata_features':0,'pre_metadata_features_metadata':1,'post_metadata_features':0})
				bm = 'unknown behavioral_mode'
				#for j in range(len(_['behavioral_modes'])):
				#	if mv[-(j+1),0,0]:
				#		bm = _['behavioral_modes'][j]
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
				plot(ov,'o-g'); plot(tv,'o-r'); plt.title(D['names'][0])
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

		if _['loss_timer'].check() and len(_['LOSS_LIST_AVG'])>5:
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
			u = min(len(_['LOSS_LIST_AVG']),250)
			median_val = np.median(na(_['LOSS_LIST_AVG'][-u:]))
			plt.title(d2s('1000*median =',dp(1000.0*median_val,3)))
			plot([0,q],[median_val,median_val],'r')
			#plt.xlim(0,q);plt.ylim(0,0.03)
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
