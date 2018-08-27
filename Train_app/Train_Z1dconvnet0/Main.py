
#from Parameters_Module import *
from kzpy3.vis2 import *
import torch

for a in Arguments.keys():
	P[a] = Arguments[a]
	spd2s(a,'=',P[a])


#import Batch_Module
import kzpy3.Train_app.Train_Z1dconvnet0.Network_Module as Network_Module
exec(identify_file_str)

#unix('mkdir -p '+opj(P['NETWORK_OUTPUT_FOLDER'],'weights'))

Network = Network_Module.Pytorch_Network()


#Batch = Batch_Module.Batch(the_network=Network)
display_timer = Timer(10)

while True:
	#the_input = np.zeros((2,12,50))
	#the_target = np.zeros((2,20,1))
	the_input = torch.randn(2,12,150)
	the_target = torch.randn(2,20,1)
	the_target[0,0:10,0]=torch.from_numpy(na([1,2,3,4,5,6,7,8,9,10]))
	the_target[1,0:10,0]=torch.from_numpy(na([1,2,3,4,5,6,7,8,9,10]))

	Network['forward'](the_input,the_target)
	#Network['forward'](torch.randn(2,12,150),torch.randn(2,20,1))
	Network['backward']()
	if display_timer.check():
		for l in ['input','conv1','conv2','avg']:
			mi(Network['net'].P[l][0],l)
		print(the_target)
		spause()
		display_timer.reset()
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