#

from Parameters_Module import *

for a in Args.keys():
	b = Args[a]
	if str_is_int(b):
		b = int(b)
	P[a] = b
	spd2s(a,'=',P[a])



import Batch_Module
import Network_Module
exec(identify_file_str)




for folder in ['weights']:
	unix('mkdir -p '+opj(P[NETWORK_OUTPUT_FOLDER],folder))


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