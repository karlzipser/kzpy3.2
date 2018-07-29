###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Train_app/Train_SqueezeNet_indoor_aruco__2','kzpy3/teg9'])
#
###############################
from Parameters_Module import *
import Batch_Module
import Network_Module
exec(identify_file_str)



for a in Args.keys():
    P[a] = Args[a]


# save loss records for train and val, times and moment numbers
# save loss by moment id
# save weights
# save other state variables
#current_code_dst_folder = opj(code,time_str())
#for folder in [code,current_code_dst_folder,loss_history,weights]:
#	unix('mkdir -p '+opj(P[NETWORK_OUTPUT_FOLDER],folder))
#unix('scp -r '+P[CODE_PATH]+' '+opj(P[NETWORK_OUTPUT_FOLDER],current_code_dst_folder))





n_to_use = 300
np.random.shuffle(P['all_image_file_paths'])
np.random.shuffle(P['all_flip_image_file_paths'])
current_runs = P['all_image_file_paths'][:n_to_use]
current_flip_runs = P['all_flip_image_file_paths'][:n_to_use]


All_image_files = {}
folders5 = sgg('/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/h5py/*')
for f in folders5:
	print fname(f)
	All_image_files[fname(f)] = {}
	if True:
		try:
			O = h5r(opj(f,'original_timestamp_data.h5py'))
			F = h5r(opj(f,'flip_images.h5py'))
			All_image_files[fname(f)]['normal'] = O
			All_image_files[fname(f)]['flip'] = F
		except Exception as e:
			print("********** Exception ***********************")
			print(e.message, e.args)	
P['All_image_files'] = All_image_files





Network = Network_Module.Pytorch_Network()


Batch = Batch_Module.Batch(network,Network)



while True:

	Batch[clear]()

	Batch[fill](data,None, mode,None)

	Batch[forward]()

	Batch[display]()

	Batch[backward]()

	Network[save_net]()

	








#EOF