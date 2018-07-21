from kzpy3.utils2 import *

Network = {}
Network['network_output_sample'] = 4 # >= 0, <= 9
Network['network_steer_gain'] = 3.0
Network['network_motor_gain'] = 0.75
Network['network_motor_offset'] = 0
Network['network_smoothing_parameter'] = 0.33
Network['weight_file_path'] = opjh('pytorch_models','net.infer')
Network['USE_NETWORK'] = True

Mse = {}
Mse['HUMAN_SMOOTHING_PARAMETER_1'] = 0.75
Mse['USE_MSE'] = True
Mse['USE_SIG'] = True
Mse['USE_IMU'] = True

NO_Mse = {}
NO_Mse['behavioral_mode_choice'] = 'furtive'
NO_Mse['place_choice'] = 'Tilden'

Record = {}
Record['RECORD_DATA'] = True



"""
-figure out how pytorch model works
-make new verwion based on dicts which I use in both training and driving
-make input format flexible (e.g., frames, metadat, etc)
-get workstation going
-avoid getting bogged down in non-essential coding
-have network output all behavioral trajectories
	this reqires training a net using output of net to get non-data trajectories
-timestamp network output predictions so that these can be used in real time.
-set up Sascha cars
-think about depth map, either from algorithim or camera
-figure out how to process bag data (there are two apps for this)
-think about smaller res network
-write down all images sizes
-find model used for demo
-display images of various scales in real time as demo
"""