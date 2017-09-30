#!/usr/bin/env python

from Parameters_Module import *
import Batch_Module
import Network_Module
exec(identify_file_str)


for a in Args.keys():
    P[a] = Args[a]

Network = Network_Module.Pytorch_Network()

Batch = Batch_Module.Batch(network=Network)

open_some_files_timer = Timer(10*60)


while True:

	Batch[CLEAR]()

	Batch[FILL](data=None,mode=None)

	Batch[FORWARD]()

	Batch[DISPLAY]()

	Batch[BACKWARD]()

	Network[SAVE_NET]()

	








#EOF