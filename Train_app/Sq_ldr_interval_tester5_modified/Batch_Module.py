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
	_['ref_run'] = {}
	_['other_run'] = {}

	Data_Module.prepare_data_for_training(_)

	zero_matrix = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()
	one_matrix = torch.FloatTensor(1, 1, 23, 41).fill_(1).cuda()
	temp = (255*z2o(np.random.randn(94,168))).astype(np.uint8)
	zero_94_168_img = zeros((94,168),np.uint8)
	zero_94_168_3_img = zeros((94,168,3),np.uint8)
	zero_23_41_3_img = np.zeros((23,41,3),np.uint8)



		


	def _function_fill(ref_run,ref_index,ref_image,other_run,other_index,other_image):
	
		assert type(ref_run) == str
		assert type(ref_index) == int
		assert type(ref_image) == np.ndarray

		assert type(other_run) == str
		assert type(other_index) == int
		assert type(other_image) == np.ndarray

		"""
		_['ref_run']['Imgs'] = ref_image
		_['ref_run']['index'] = ref_index
		_['ref_run']['name'] = ref_run

		_['other_run']['Imgs'] = other_image
		_['other_run']['index'] = other_index
		_['other_run']['name'] = other_run
		"""



		list_camera_input = []
		list_camera_input.append(torch.from_numpy(ref_image))
		list_camera_input.append(torch.from_numpy(other_image))
		list_camera_input.append(torch.from_numpy(zero_23_41_3_img))
		list_camera_input.append(torch.from_numpy(zero_23_41_3_img))

		camera_data = torch.cat(list_camera_input, 2)

		camera_data = camera_data.cuda().float()/255. - 0.5
		camera_data = torch.transpose(camera_data, 0, 2)
		camera_data = torch.transpose(camera_data, 1, 2)
		D['camera_data'] = torch.cat((torch.unsqueeze(camera_data, 0), D['camera_data']), 0)


		_['frequency_timer'].freq(d2s('train duration =',int(_['duration timer'].time()),"\t"))
	








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
		#D['loss'] = D['network']['criterion'](D['outputs'], torch.autograd.Variable(D['target_data']))
		value = D['outputs'].data.cpu().numpy()[0][0]

		return value


		




	D['FILL'] = _function_fill
	D['CLEAR'] = _function_clear
	D['FORWARD'] = _function_forward
	#D['BACKWARD'] = _function_backward
	#D['DISPLAY'] = _function_display
	#D['ACCUMULATE_RESULTS'] = _function_accumlate_results


	return D






#EOF
