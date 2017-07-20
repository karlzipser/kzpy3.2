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










Network = Network_Module.Pytorch_Network()

Training_data = Data_Module.Training_Data()

Batch = Batch_Module.Batch(network,Network)

timer = Timer(0)

while True:
	timer.reset()
	Batch[clear]()
	Batch[fill]('Data',Training_data, mode,train)
	Batch[forward]()
	Batch[display](print_now,True)
	Batch[backward]()
	print timer.time()
	

	#Batch['clear']()






#EOF