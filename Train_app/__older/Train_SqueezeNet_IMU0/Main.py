#!/usr/bin/env python

from Parameters_Module import *
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
#current_code_dst_folder = opj(code,time_str())
#for folder in [code,current_code_dst_folder,loss_history,weights]:
#	unix('mkdir -p '+opj(P[NETWORK_OUTPUT_FOLDER],folder))
#unix('scp -r '+P[CODE_PATH]+' '+opj(P[NETWORK_OUTPUT_FOLDER],current_code_dst_folder))




Network = Network_Module.Pytorch_Network()


Batch = Batch_Module.Batch(network,Network)

open_some_files_timer = Timer(10*60)


while True:


	Batch[clear]()

	Batch[fill](data,None, mode,None)

	Batch[forward]()

	Batch[display]()

	Batch[backward]()

	Network[save_net]()

	








#EOF