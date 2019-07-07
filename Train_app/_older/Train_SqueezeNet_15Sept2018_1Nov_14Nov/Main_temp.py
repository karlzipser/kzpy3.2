from kzpy3.utils3 import *
# This app used for extensive training.
from kzpy3.Train_app.Train_SqueezeNet_15Sept2018_1Nov_14Nov.default_values import *

startup_timer = Timer()


#from Parameters_Module import *

for a in Arguments.keys():
	P[a] = Arguments[a]
print_Arguments()

P['print_timer'] = Timer(P['print_timer_time'])
P['loss_timer'] = Timer(P['loss_timer_time'])
P['menu_load_timer'] = Timer(P['menu_load_timer_time'])
P['spause_timer'] = Timer(P['spause_timer_time'])
if P['trigger print timer?']:
	P['print_timer'].trigger()
P['reload_image_file_timer'] = Timer(P['reload_image_file_timer_time'])
if P['trigger loss_timer?']:
	P['loss_timer'].trigger()


import kzpy3.Train_app.Train_SqueezeNet_15Sept2018_1Nov_14Nov.Batch_Module as Batch_Module
import kzpy3.Train_app.Train_SqueezeNet_15Sept2018_1Nov_14Nov.Network_Module as Network_Module
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

	if True:
		for channel in range(P['BATCH_SIZE']):
			show_color_net_inputs(
				Network['net'].A['camera_input'],
				Network['net'].A['pre_metadata_features_metadata'],channel)
			raw_enter(d2s(channel,'\t'))

	Batch['DISPLAY']()

	Batch['BACKWARD']()



	




	



#EOF