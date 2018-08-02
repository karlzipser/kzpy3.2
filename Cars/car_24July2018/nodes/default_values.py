from kzpy3.utils2 import *

Network = {}
Network['network_output_sample'] = 4 # >= 0, <= 9
Network['network_steer_gain'] = 3.0
Network['network_motor_gain'] = 1.0
Network['network_motor_offset'] = 0
Network['network_smoothing_parameter'] = 0.75
#Network['weight_file_path'] = opjh('pytorch_models','epoch6goodnet.SqueezeNet')
#Network['weight_file_path'] = opjh('pytorch_models','net_17Sep17_17h21m35s.SqueezeNet')
Network['weight_file_path'] = opjh('pytorch_models','net_10Jun18_00h00m45s.SqueezeNet')
Network['USE_NETWORK'] = True
Network['GREY_OUT_TOP_OF_IMAGE'] = False
Network['visualize_activations'] = False
Network['motor_reverse_threshold'] = 55

Mse = {}
Mse['HUMAN_SMOOTHING_PARAMETER_1'] = 0.75
Mse['USE_MSE'] = True
Mse['USE_SIG'] = True
Mse['USE_IMU'] = True

NO_Mse = {}
NO_Mse['behavioral_mode_choice'] = 'direct'
NO_Mse['place_choice'] = 'home'

"""
https://stackoverflow.com/questions/29232438/bash-check-if-var-is-in-number-range
https://stackoverflow.com/questions/806906/how-do-i-test-if-a-variable-is-a-number-in-bash
https://unix.stackexchange.com/questions/157960/input-two-numbers-and-add-them-when-a-is-typed-subtract-when-s-is-typed
https://stackoverflow.com/questions/34171568/return-value-from-python-script-to-shell-script
https://askubuntu.com/questions/639100/how-to-get-connection-to-both-wifi-as-well-as-lan-in-ubuntu-14-04-lts
https://www.programcreek.com/python/example/107643/torch.nn.Conv1d

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


export DISPLAY=:0.0
from kzpy3.vis2 import *
mi(np.random.random((100,100)))


3840x2160

nmcli radio wifi off
nmcli radio wifi on

-make playback with LCR visualization; timestamp predictions, show current and past ones, in different grays
-train network to output all three predictinos
-work on 2 zed car, give it back standard rear axel; setup tx2 as forward jetson; work out ethernet connection
-see about running models in threads
-learn encoder values 
-consider not bringing images together until after some procesing
-find LCR data
-net with color vs motion for two camerass in initial layers
-set up arena?
-figure out why raised arena always yields heading pause.
-back up training data

(left,-1,red)
(left,-1,green)
(left,-1,blue)
(left,-2,green)
(right,-1,green)
(right,-2,green)
(right,-3,green)
(right,-4,green)
(right,-5,green)
(right,-6,green)
(right,-7,green)
(right,-8,green)

-if a net gets trajectory predictions plus velocity estimate, it can choose which output point to use.
-not that authorized_keys has moved, fix this on cars.
-figure out how to backup data, how to preprocess LCR and new left-center-right
-label new data folders
-have a 'stop' behavioral mode controlled by transmitter to get non-aruco heading pause data
-note the need to fix baseline problem with LCR files from June, and check that same problem isn't happening now

http://wiki.ros.org/ROS/NetworkSetup
https://answers.ros.org/question/90536/ros-remote-master-can-see-topics-but-no-data/
https://answers.ros.org/question/118576/rostopic-publish-message-to-remote-machine/
export ROS_MASTER_URI=http://192.168.1.20:11311
make sure master's ip and name (tegra-ubuntu) are in /etc/hosts
on master, export ROS_IP=0.0.0.0 # Listen on any interface

ipaddr_ = "http://192.168.1.20:11311"
print(d2s('Setting ROS_MASTER_URI to',ipaddr_))
os.environ["ROS_MASTER_URI"] = ipaddr_
os.environ["ROS_IP"] = "0.0.0.0"

on publisher (.101)
export ROS_IP=192.168.1.101
roscore 
in /etc/hosts "192.168.1.50 laptop", the name laptop being important it seems. Get this by typing 'hostname' on command line.
on subscriber machine, ROS_IP='' [do not set] (may not be necessary)


"""