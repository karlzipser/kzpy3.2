#!/usr/bin/env python

from Parameters_Module import *
import Batch_Module
import Network_Module
import Runs_Module
import Data_Packer_Module
exec(identify_file_str)

for a in Args.keys():
	pd2s("Args[",a,"] =",Args[a])
    P[a] = Args[a]

Runs = Runs_Module.Runs()

Data_packer = Data_Packer_Module.Data_Packer(RUNS=Runs)

Network = Network_Module.Pytorch_Network()

Batch = Batch_Module.Batch(NETWORK=Network,DATA_PACKER=Data_packer)

while True:

	Batch[FILL]()

	Batch[FORWARD]()

	Batch[DISPLAY]()

	Batch[BACKWARD]()

	Network[SAVE_NET]()

	

#EOF