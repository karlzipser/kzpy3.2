from kzpy3.utils3 import *
exec(identify_file_str)



P = {}
P['agent_is_human'] = True
P['use_motor_PID'] = False

P['customers'] = ['Arduino Node','Network Node',' Trained Nets']
P['drive_mode'] = 0
P['use LIDAR'] = False
P['use sound'] = True
P['use flex'] = True
P['max motor'] = 63
P['show_net_input'] = False
P['show_net_activity'] = False
P['menu name'] = 'arduino menu'
P['cmd/autostart menu'] = False
P['cmd/clear_screen'] = False
P['use menu'] = True
P['zed_called'] = {}
P['zed_called']['val'] = 0
P['zed_called']['time'] = 0
P['os1_called'] = {}
P['os1_called']['val'] = 0
P['os1_called']['time'] = 0
P['print_timer time'] = 0.1
P['IMU/print_timer'] = Timer(P['print_timer time'])
P['MSE/print_timer'] = Timer(P['print_timer time'])
P['temporary_human_control'] = False
P['acc triggers'] = 'shutdown'
P['car_name'] = os.environ["COMPUTER_NAME"]
P['calibrated'] = False
P['ABORT'] = False

P['servo_percent'] = 49
P['motor_percent'] = 49
P['LED_number'] = {}
P['LED_number']['current'] = 0
P['CALIBRATION_NULL_START_TIME'] = 3.0
P['CALIBRATION_START_TIME'] = 4.0
P['print_mse_freq'] = False
P['print_imu_freq'] = False
P['print_calibration_freq'] = False
P['print_selector_freq'] = False
P['print_led_freq'] = False
P['USE_ROS'] = HAVE_ROS # using_linux()
P['human'] = {}
P['human']['servo_percent'] = 49
P['human']['motor_percent'] = 49
P['network'] = {}
P['network']['servo_percent'] = 49
P['network']['motor_percent'] = 49
P['IMU_SMOOTHING_PARAMETER'] = 0.95
P['Hz'] = {}
P['servo_pwm_null'] = 1450
P['motor_pwm_null'] = P['servo_pwm_null']
P['servo_pwm_min'] = P['servo_pwm_null']
P['servo_pwm_max'] = P['servo_pwm_null']
P['motor_pwm_min'] = P['servo_pwm_null']
P['motor_pwm_max'] = P['servo_pwm_null']
P['behavioral_mode_choice'] = 'direct'
P['place_choice'] = 'local'

if P['car_name'] == 'Mr_Blue_Back':
	P['servo_pwm_smooth_manual_offset'] = -30
	P['camera_pwm_manual_offset'] = -500
	P['servo_feedback_center'] = 214
	P['servo_feedback_right'] = 140
	P['servo_feedback_left'] = 294
else:
	P['servo_pwm_smooth_manual_offset'] = 0
	P['camera_pwm_manual_offset'] = 0	

P['HUMAN_SMOOTHING_PARAMETER_1'] = 0.75
P['USE_MSE'] = True
#P['USE_SIG'] = True
P['USE_IMU'] = True

P['pid_motor_slope'] = (60-49)/3.0
P['pid_motor_gain'] = 0.05
P['pid_encoder_max'] = 4.0
P['pid_motor_encoder_max'] = 4.0
P['pid_motor_delta_max']= 0.05
P['pid_motor_percent_max']= 99
P['pid_motor_percent_min']= 0
P['pid_steer_gain']= 0.05
P['pid_steer_delta_max']= 0.05
P['pid_steer_steer_percent_max']= 99
P['pid_steer_steer_percent_min'] = 0
P['use_servo_feedback'] = 0

P['button_delta'] = 50
P['button_number'] = 0
P['button_timer'] = Timer()
P['time_since_button_4'] = Timer()
P['servo_pwm_smooth'] = 1000
P['motor_pwm_smooth'] = 1000
#P['selector_mode'] = False
P['encoder_smooth'] = 0.0
P['network']['camera_percent'] = 49
P['Hz']['mse'] = 0
P['calibrated'] = False
P['acc'] = {}
P['gyro'] = {}
P['head'] = {}
#P['The menu path.'] = opjk('Cars/car_24July2018/nodes/Default_values/arduino')
P['autostart menu'] = False


flex_names = [
	'FL0',
	'FL1',
	'FL2',
	'FL3',
	'FR0',
	'FR1',
	'FR2',
	'FR3',
	'FC0',
	'FC1',
	'FC2',
	'FC3',
]

for f in flex_names:
    P[f] = {}
P['to_hide'] = []

P['To Expose'] = {}
P['To Expose']['Arduino Node'] = [
	'ABORT',
	'IMU_SMOOTHING_PARAMETER',
	'behavioral_mode_choice',
	'agent_is_human',
	'place_choice',
	'servo_pwm_smooth_manual_offset',
	'camera_pwm_manual_offset',
	'pid_motor_slope',
	'pid_motor_gain',
	'pid_encoder_max',
	'pid_motor_delta_max',
	'pid_motor_percent_max',
	'pid_motor_percent_min',
	'menu name',
	'use LIDAR',
	'use sound',
	'use_motor_PID',
]

P['To Expose']['Network Node'] = [
	'network_output_sample',
	'network_steer_gain',
	'network_camera_gain',
	'network_motor_gain',
	'network_motor_offset',
	'network_servo_smoothing_parameter',
	'network_motor_smoothing_parameter',
	'network_camera_smoothing_parameter',
	'USE_LAST_IMAGE_ONLY',
	'LOAD NETWORK',
	'max motor',
	'show_net_input',
	'show_net_activity',
]

def sort_dir_by_ctime(dir_path):
	"""
	https://www.w3resource.com/python-exercises/python-basic-exercise-71.php
	"""
	from stat import S_ISREG, ST_MTIME, ST_MODE
	import os, sys, time
	data = (os.path.join(dir_path, fn) for fn in os.listdir(dir_path))
	data = ((os.stat(path), path) for path in data)
	# regular files, insert creation date
	data = ((stat[ST_MTIME], path)
	           for stat, path in data if S_ISREG(stat[ST_MODE]))
	paths = []
	for cdate, path in sorted(data):
	    #print(os.path.basename(path),time.ctime(cdate))
	    paths.append(path)
	return paths

try:
	P['To Expose']['Trained Nets'] = []
	P['weight_files'] = {}
	Model_folders = {}
	for f in sggo(opjm("rosbags/networks/*")):
	#for f in sort_dir_by_ctime(opjm("rosbags/networks/*")):
	#for f in sggo(opjk("Cars/*")):
		#Model_folders[opj(fname(f),'count')] = len(sggo(f,'*'))
		weight_files = sort_dir_by_ctime(f)
		l = len(weight_files)
		n = d2n(fname(f)," (",l,")")
		P[n] = [False]
		P['To Expose']['Trained Nets'].append(n)
		P['weight_files'][n] = weight_files

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    CS_('Exception!',emphasis=True)
    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

P['LOAD NETWORK'] = False

############# NETWORK PARAMETERS
P['network_output_sample'] = 0 # >= 0, <= 9
P['network_steer_gain'] = 1.0#6.0
P['network_camera_gain'] = 1.0#2.0
P['network_motor_gain'] = 1.0#0.8
P['network_motor_offset'] = 0
P['network_servo_smoothing_parameter'] = 0.85
P['network_motor_smoothing_parameter'] = 0.75
P['network_camera_smoothing_parameter'] = 0.0
P['weight_file_path'] = opjh('pytorch_models/epoch6goodnet')#opjD('link_to_weights_file.SqueezeNet')#opjh('pytorch_models','net_10Jun18_00h00m45s.SqueezeNet')
P['USE_NETWORK'] = True
P['GREY_OUT_TOP_OF_IMAGE'] = False
P['USE_LAST_IMAGE_ONLY'] = False
P['visualize_activations'] = False
###########################








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
-net with color vs motion for two cameras in initial layers
-set up arena?
-figure out why raised arena always yields heading pause.
-back up training data


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

-make driving mode with drive and collision
-set up arena
-set up TX2 for data collection car and collect depth data
-collect l,c,r outputs of network, use output with max motor value.
 -harden Mr_Blue
https://www.danielandrade.net/2016/10/30/interfacing-two-adafruit-mma8451-via-i2c/
http://forums.trossenrobotics.com/tutorials/how-to-diy-128/get-position-feedback-from-a-standard-hobby-servo-3279/
http://forums.trossenrobotics.com/tutorials/how-to-diy-128/cheap-battery-monitor-using-resistive-voltage-divider-3264/
https://www.hackster.io/SHAHIR_nasar/simple-homemade-flex-sensor-ff54f0
https://www.instructables.com/id/DIY-Flex-Sensor-Under-1-/
https://www.tekrevue.com/tip/how-to-create-a-4gbs-ram-disk-in-mac-os-x/
https://answers.ros.org/question/239968/how-do-you-implement-a-rospy-keyboardinterrupt-without-killing-the-node/
https://www.instructables.com/id/How-to-Make-Bi-Directional-Flex-Sensors/

need to:
 fix wheel encoder
add second wheel encoder
move and reverse some flex sensors
make battery packs
 have it so body does not have to be on to play disk. Need releasable clip on usb3 cable
	second LED to: show bagfile count, show wifi status, other critical things
fix wheel and camera alignment
record C calibration settings

2nd LED:
	count bag files (64 red, then green the yellow) or write text
	list working arduinos
	wifi status
	network status

Revisit tx1 to tx1 ros networking.

https://devtalk.nvidia.com/default/topic/1002271/pins-for-front-panel-buttons-led/

"""




