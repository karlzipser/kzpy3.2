###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/pytorch3/Train_SqueezeNet','kzpy3/teg9'])
#
###############################
from Parameters_Module import *
import Data_Module
import Batch_Module
import Network_Module
exec(identify_file_str)

_ = dictionary_access

for a in Args.keys():
    _(P,a,equals,_(Args,a)) #P[a] = Args[a]


# save loss records for train and val, times and moment numbers
# save loss by moment id
# save weights
# save other state variables
current_code_dst_folder = opj(code,time_str())
for folder in [code,current_code_dst_folder,loss_history,weights]:
	unix('mkdir -p '+opj(P[NETWORK_OUTPUT_FOLDER],folder))
unix('scp -r '+P[CODE_PATH]+' '+opj(P[NETWORK_OUTPUT_FOLDER],current_code_dst_folder))



Network = Network_Module.Pytorch_Network()

Train_Val_data = Data_Module.Training_Data()

Batch = Batch_Module.Batch(network,Network)

timer = Timer(0)

while True:
	for train_val in [
		[train,val,Timer(P[TRAIN_TIME]),'b'],
		[val,train,Timer(P[VAL_TIME]),'r']]:

		modev = train_val[0]
		other_modev = train_val[1]
		timer = train_val[2]
		timer.reset()
		colorv = train_val[3]
		while not timer.check():
			Batch[clear]()
			Batch[fill](data,Train_Val_data, mode,modev)
			Batch[forward]()
			Batch[display]()
			Batch[backward]()
			Network[loss_record][modev][add](loss,Batch['loss'].data.cpu().numpy()[0],
				'alt_ctr',Network[loss_record][other_modev][ctr],
				'color',colorv)
			Network[save_net]()

	

	#Batch['clear']()






#EOF