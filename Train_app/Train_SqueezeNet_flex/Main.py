
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

unix('mkdir -p '+opj(P['NETWORK_OUTPUT_FOLDER'],'weights'))

Network = Network_Module.Pytorch_Network()

Batch = Batch_Module.Batch(the_network=Network)


while True:
	
	#try:

	Batch['CLEAR']()

	Batch['FILL']()

	Batch['FORWARD']()
	#cs('main1')
	Batch['DISPLAY']()
	#cs('main2')
	Batch['BACKWARD']()

	Network['SAVE_NET']()
	#except:
	#	print 'FAIL'

	
	



#EOF