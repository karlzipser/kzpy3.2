
from Parameters_Module import *

for a in Arguments.keys():
	P[a] = Arguments[a]
print_Arguments()

P['print_timer'] = Timer(P['print_timer_time'])
P['reload_image_file_timer'] = Timer(P['reload_image_file_timer_time'])

import Batch_Module
import Network_Module
exec(identify_file_str)

unix('mkdir -p '+opj(P['NETWORK_OUTPUT_FOLDER'],'weights'))

Network = Network_Module.Pytorch_Network()

Batch = Batch_Module.Batch(the_network=Network)


    

    

    






while P['ABORT'] == False:

	Batch['CLEAR']()

	Batch['FILL']()

	Batch['FORWARD']()

	Batch['DISPLAY']()

	Batch['BACKWARD']()

	Network['SAVE_NET']()




	



#EOF