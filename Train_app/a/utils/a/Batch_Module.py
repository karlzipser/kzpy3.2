from Parameters_Module import *
exec(identify_file_str)
from vis2 import *
import torch
import torch.nn.utils as nnutils
import Activity_Module

if True: pythonpaths(['kzpy3','kzpy3/Train_app/Train_SqueezeNet_IMU1','kzpy3/teg9']) # temp

# 1/4 original image shape = (94, 168, 3)
# metadata x-y shape = (23,41)

zero_matrix = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()
one_matrix = torch.FloatTensor(1, 1, 23, 41).fill_(1).cuda()




def Batch(**Args):

	for we_are in ["the setup section"]:

		_ = {}
		_[NETWORK] = Args[NETWORK]
		_[DATA_PACKER] = Args[DATA_PACKER]

		_[BATCH_SIZE] = P[BATCH_SIZE]
		_[IMAGE_DATA] = torch.FloatTensor().cuda()
		_[METADATA] = torch.FloatTensor().cuda()
		_[TARGET_DATA] = torch.FloatTensor().cuda()
		_[NAMES] = []



	for we_are in ['function definitions']:

		def _function_fill(**Args):

			_function_clear()


			for we_are in ['a helper function definition']:

				def _function_data_into_batch():

					for we_are in ["the setup section"]:

						name,list_of_images,list_of_meta_data_floats_or_arrays,list_of_target_floats_or_lists = _[DATA_PACKER][NEXT]()
						assert(6*P[N_FRAMES] == len(list_of_images))
						_[NAMES].insert(0,name) # This to match torch.cat use below
						#print name
					for we_are in ["the image section"]:

						list_of_torch_images = []
						for img in list_of_images:
							#print shape(img)
							assert(shape(img)==(94, 168, 1))
							list_of_torch_images.append(torch.from_numpy(img))

						torch_img_data = torch.cat(list_of_torch_images, 2) #? what does this do?
						torch_img_data = torch_img_data.cuda().float()/255. - 0.5
						torch_img_data = torch.transpose(torch_img_data, 0, 2)
						torch_img_data = torch.transpose(torch_img_data, 1, 2)
						_[IMAGE_DATA] = torch.cat((_[IMAGE_DATA],torch.unsqueeze(torch_img_data, 0)), 0)

					for we_are in ["the metadata section"]:

						metadata_ctr = 0

						torch_metadata = torch.FloatTensor().cuda()

						for metadata_value in list_of_meta_data_floats_or_arrays:

							if metadata_value == 0.0:

								torch_metadata = torch.cat((zero_matrix, torch_metadata), 1); metadata_ctr += 1

							elif metadata_value == 1.0:

								torch_metadata = torch.cat((one_matrix, torch_metadata), 1); metadata_ctr += 1
							
							else:
								assert(False)		

						for i in range(128 - metadata_ctr): # Concatenate zero matrices to fit the dataset
							torch_metadata = torch.cat((zero_matrix, torch_metadata), 1)

						_[METADATA] = torch.cat((torch_metadata, _[METADATA]), 0)



					for we_are in ["the target section"]:
						target_list = []
						for d in list_of_target_floats_or_lists:
							if type(d) == list:
								target_list += d
							else:
								assert(is_number(d))
								target_list.append(d)
						target_data = torch.from_numpy(na(target_list)).cuda().float()
						target_data = torch.unsqueeze(torch.cat((target_data,), 0), 0)
						
						_[TARGET_DATA] = torch.cat((target_data, _[TARGET_DATA]), 0)


			for we_are in ['the main batch fill loop']:
				ctr = 0
				_[DATA_PACKER][RUNS][INSURE_CORRECT_NUMBER_OF_RUNS_ARE_OPEN]()
				while ctr < _[BATCH_SIZE]:
					if True:#try:
						_function_data_into_batch()
						ctr += 1
						P[FREQUENCY_TIMER].freq()
					else: #except Exception as e:
						print("********** def _function_fill(*args): Exception ***********************")
						print(e.message, e.args)





		def _function_clear():
			_[IMAGE_DATA] = torch.FloatTensor().cuda()
			_[METADATA] = torch.FloatTensor().cuda()
			_[TARGET_DATA] = torch.FloatTensor().cuda()
			_[NAMES] = []
			_[OUTPUTS] = None
			_[LOSS] = None


		def _function_forward():
			Trial_loss_record = _[NETWORK][data_moment_loss_record]
			_[NETWORK][optimizer].zero_grad()
			_[OUTPUTS] = _[NETWORK][NET](torch.autograd.Variable(_[IMAGE_DATA]), torch.autograd.Variable(_[METADATA])).cuda()
			_[LOSS] = _[NETWORK][criterion](_[OUTPUTS], torch.autograd.Variable(_[TARGET_DATA]))


		def _function_backward():
			_[LOSS].backward()
			nnutils.clip_grad_norm(_[NETWORK][NET].parameters(), 1.0)
			_[NETWORK][optimizer].step()
			P['LOSS_LIST'].append(_[LOSS].data.cpu().numpy()[:].mean())
			if len(P['LOSS_LIST']) > 100:
				P['LOSS_LIST_AVG'].append(na(P['LOSS_LIST']).mean())
				P['LOSS_LIST'] = []


		def _function_display(*args):
			Args = args_to_dictionary(args)
			if print_now not in Args:
				Args[print_now] = False
			cv2.waitKey(1) # This is to keep cv2 windows alive
			if P[PRINT_TIMER].check() or Args[print_now]:

				ov = _[OUTPUTS][0].data.cpu().numpy()
				mv = _[METADATA][0].cpu().numpy()
				tv = _[TARGET_DATA][0].cpu().numpy()

				print('Loss:',dp(_[LOSS].data.cpu().numpy()[0],5))

				if P[LOSS_TIMER].check():
					figure('LOSS_LIST_AVG');clf();plot(P['LOSS_LIST_AVG'],'.')
					P[LOSS_TIMER].reset()
				if True:
					Net_activity = Activity_Module.Net_Activity(ACTIVATIONS=_[NETWORK][NET].A)
					Net_activity[view](moment_index,0,delay,33, scales,{camera_input:3,pre_metadata_features:0,pre_metadata_features_metadata:2,post_metadata_features:4})

					figure('steer')
					clf()
					ylim(-0.05,1.05);xlim(0,len(tv))
					plot([-1,60],[0.49,0.49],'k');plot(ov,'og'); plot(tv,'or'); plt.title(_[NAMES][0])
					figure('METADATA');clf()
					plot(mv[-10:,0,0],'r.-')
					spause()

					P[PRINT_TIMER].reset()

	for we_are in ['the place where we name the functions']:

		_[FILL] = _function_fill
		#_[CLEAR] = _function_clear
		_[FORWARD] = _function_forward
		_[BACKWARD] = _function_backward
		_[DISPLAY] = _function_display


	for we_are in ['the return section.']:
	
		return _



#EOF
