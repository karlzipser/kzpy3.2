#!/usr/bin/env python
if False:
	pythonpaths(['kzpy3','kzpy3/Train_app/a/nets/Train_SqueezeNet_IMU','kzpy3/Train_app/a/utils/a'])
from Parameters_Module import *
import Batch_Module
import Network_Module
import Data_Packer_Module
exec(identify_file_str)


#for a in Args.keys():
#    P[a] = Args[a]

Data_packer = Data_Packer_Module.Data_Packer()

Network = Network_Module.Pytorch_Network()

Batch = Batch_Module.Batch(NETWORK=Network,DATA_PACKER=Data_packer)

#open_some_files_timer = Timer(10*60)


while True:

	#Batch[CLEAR]()

	Batch[FILL]()

	Batch[FORWARD]()

	Batch[DISPLAY]()

	Batch[BACKWARD]()

	Network[SAVE_NET]()

	








#EOF