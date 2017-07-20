##############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/pytorch3/Train_SqueezeNet','kzpy3/teg9'])
#
##############################
from Parameters_Module import *
import Data_Module
import Batch_Module
import Network_Module
exec(identify_file_str)

_ = dictionary_access

for a in Args.keys():
    _(P,a,equals,_(Args,a)) #P[a] = Args[a]



trial_loss_record = {} # get this into Pytorch_Network







Network = Network_Module.Pytorch_Network()

Training_data = Data_Module.Training_Data()

Batch = Batch_Module.Batch(net,Network[net], batch_size,P[BATCH_SIZE])

timer = Timer(0)

while True:
	timer.reset()
	Batch[clear]()
	Batch[fill]('Data',Training_data, mode,train)
	Batch[forward]({'optimizer':Network[optimizer],'criterion':Network[criterion],'trial_loss_record':trial_loss_record})
	Batch[display]({'print_now':True})
	Batch[backward]({'optimizer':Network[optimizer]})
	print timer.time()
	

	#Batch['clear']()






#EOF