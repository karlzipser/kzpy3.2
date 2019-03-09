from kzpy3.vis3 import *
import Data_Module
import torch
import torch.nn.utils as nnutils
import Activity_Module
exec(identify_file_str)

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
	_['results'] = {}
	_['results']['target'] = []
	_['results']['output'] = []
	if 'LOSS_LIST_AVG' not in _:
		_['LOSS_LIST_AVG'] = []
	_['reload_image_file_timer'].trigger()

	Data_Module.prepare_data_for_training(_)

	zero_matrix = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()
	one_matrix = torch.FloatTensor(1, 1, 23, 41).fill_(1).cuda()
	temp = (255*z2o(np.random.randn(94,168))).astype(np.uint8)
	zero_94_168_img = zeros((94,168),np.uint8)

	files = sggo('/home/karlzipser/Desktop/Data/Network_Predictions_projected/*.net_projections.h5py')
	GOOD_LIST = []
	for f in files:
	    GOOD_LIST.append(fname(f).split('.')[0])





	def _function_fill():

		while _['ABORT'] == False:
			if True:#try:
	
				###################################################################
				###################################################################
				###################################################################
				#### CAMERA DATA


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


				




				_['frequency_timer'].freq(d2s('train duration =',int(_['duration timer'].time()),"\t"))
			else: #except Exception as e:
				print("*** while ctr < D['batch_size']: ******* Exception ***********************")
				print(e.message, e.args)








	def _function_clear():
		D['camera_data'] = torch.FloatTensor().cuda()
		D['outputs'] = None





	def _function_forward():
		if _['ABORT'] == True:
			return
		#Trial_loss_record = D['network'][data_moment_loss_record]
		D['network']['optimizer'].zero_grad()
		D['outputs'] = D['network']['net'](torch.autograd.Variable(D['camera_data'])).cuda()
		#D['outputs'] = D['network']['net'](torch.autograd.Variable(D['camera_data']), torch.autograd.Variable(D['metadata'])).cuda()
		D['loss'] = D['network']['criterion'](D['outputs'], torch.autograd.Variable(D['target_data']))
		_['LDR values'].append(D['outputs'].data.cpu().numpy()[0][0])
		if _['LDR timer'].check():
			_['LDR timer'] = Timer(_['LDR timer time'])
			figure(99)
			clf()
			plot(_['LDR values'],'.')


		




	D['FILL'] = _function_fill
	D['CLEAR'] = _function_clear
	D['FORWARD'] = _function_forward
	#D['BACKWARD'] = _function_backward
	#D['DISPLAY'] = _function_display
	#D['ACCUMULATE_RESULTS'] = _function_accumlate_results


	return D






#EOF
