from kzpy3.utils3 import *

startup_timer = Timer()

from Parameters_Module import *

for a in Arguments.keys():
	P[a] = Arguments[a]
print_Arguments()

P['print_timer'] = Timer(P['print_timer_time'])
if P['trigger print timer?']:
	P['print_timer'].trigger()
P['reload_image_file_timer'] = Timer(P['reload_image_file_timer_time'])
if P['trigger loss_timer?']:
	P['loss_timer'].trigger()


import Batch_Module
import Network_Module
exec(identify_file_str)

unix('mkdir -p '+opj(P['NETWORK_OUTPUT_FOLDER'],'weights'))

Network = Network_Module.Pytorch_Network()

Batch = Batch_Module.Batch(the_network=Network)

cr("\n\nTime needed for startup =",int(startup_timer.time()),"seconds.\n\n")
del startup_timer

    

   # Start training with 12 mini metadata images at 9am 12Dec2018


timer = Timer(P['run time before quitting'])



while P['ABORT'] == False:

	if timer.check():
		cg("\n\nQuitting after runing for",P['run time before quitting'],"seconds.\n\n")
		P['save_net_timer'].trigger()
		Network['SAVE_NET']()
		break

	Batch['CLEAR']()

	Batch['FILL']()

	Batch['FORWARD']()

	Batch['DISPLAY']()

	Batch['BACKWARD']()



	




	



#EOF