
#from Parameters_Module import *
from kzpy3.vis2 import *

for a in Arguments.keys():
	P[a] = Arguments[a]
	spd2s(a,'=',P[a])


#import Batch_Module
import kzpy3.Train_app.Train_Z1dconvnet0.Network_Module as Network_Module
exec(identify_file_str)

#unix('mkdir -p '+opj(P['NETWORK_OUTPUT_FOLDER'],'weights'))

Network = Network_Module.Pytorch_Network()


#Batch = Batch_Module.Batch(the_network=Network)


while True:
	Network['forward']()
	Network['backward']()
	for l in ['input','conv1','conv2','avg']:
		mi(Network['net'].P[l][0],l)
	spause()
	#mi(P['conv2'][0],'conv2-0')
	#try:

	#Batch['CLEAR']()

	#Batch['FILL']()

	#Batch['FORWARD']()

	#Batch['DISPLAY']()

	#Batch['BACKWARD']()

	#Network['SAVE_NET']()
	#except:
	#	print 'FAIL'

	
	



#EOF