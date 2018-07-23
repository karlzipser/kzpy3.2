from kzpy3.utils2 import *

Network = {}
Network['network_output_sample'] = 4 # >= 0, <= 9
Network['network_steer_gain'] = 3.0
Network['network_motor_gain'] = 0.6
Network['network_motor_offset'] = 0
Network['network_smoothing_parameter'] = 0.75
Network['weight_file_path'] = opjh('pytorch_models','epoch6goodnet.SqueezeNet')
Network['USE_NETWORK'] = True
Network['GREY_OUT_TOP_OF_IMAGE'] = False

Mse = {}
Mse['HUMAN_SMOOTHING_PARAMETER_1'] = 0.75
Mse['USE_MSE'] = True
Mse['USE_SIG'] = False
Mse['USE_IMU'] = False

NO_Mse = {}
NO_Mse['behavioral_mode_choice'] = 'furtive'
NO_Mse['place_choice'] = 'Tilden'

"""
https://stackoverflow.com/questions/29232438/bash-check-if-var-is-in-number-range
https://stackoverflow.com/questions/806906/how-do-i-test-if-a-variable-is-a-number-in-bash
https://unix.stackexchange.com/questions/157960/input-two-numbers-and-add-them-when-a-is-typed-subtract-when-s-is-typed
https://stackoverflow.com/questions/34171568/return-value-from-python-script-to-shell-script

     rostopic pub -1 /bair_car/behavioral_mode std_msgs/String the_string

http://wiki.ros.org/rostopic
-make input format flexible (e.g., frames, metadat, etc)
-avoid getting bogged down in non-essential coding
-have network output all behavioral trajectories
	this reqires training a net using output of net to get non-data trajectories
-timestamp network output predictions so that these can be used in real time.
-think about depth map, either from algorithim or camera
-figure out how to process bag data (there are two apps for this)
-think about smaller res network
-write down all images sizes

q=gg(opjh('kzpy3/Cars/*'))
for p in q:
	if os.path.isdir(p):
		print p

"""