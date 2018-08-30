from kzpy3.utils3 import *
exec(identify_file_str)
import rospy

def EXIT(restart=False,shutdown=True,kill_ros=True,_file_=''):
	rospy.signal_shutdown(d2s("default_values.EXIT(...) from",_file_,))
	CS_("""rospy.signal_shutdown("EXIT")""",_file_)
	if kill_ros:
		CS_("doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))",_file_)
		time.sleep(0.01)
		unix(opjh('kzpy3/scripts/kill_ros.sh'))
		pass
	if shutdown:
		CS_("SHUTTING DOWN!!!!!",_file_)
		time.sleep(0.01)
		unix('sudo shutdown -h now')
	if restart:
		CS_("RESTARTING!!!!!",_file_)
		time.sleep(0.01)
		unix('sudo reboot')

Parameters = {}
Parameters['temporary_human_control'] = False
Parameters['acc triggers'] = 'shutdown'
Parameters['car_name'] = os.environ["COMPUTER_NAME"]
Parameters['calibrated'] = False
Parameters['ABORT'] = False
Parameters['agent_choice'] = 'network'
Parameters['servo_percent'] = 49
Parameters['motor_percent'] = 49
Parameters['LED_number'] = {}
Parameters['LED_number']['current'] = 0
Parameters['CALIBRATION_NULL_START_TIME'] = 3.0
Parameters['CALIBRATION_START_TIME'] = 4.0
Parameters['print_mse_freq'] = False
Parameters['print_imu_freq'] = False
Parameters['print_calibration_freq'] = False
Parameters['print_selector_freq'] = False
Parameters['print_led_freq'] = False
Parameters['USE_ROS'] = HAVE_ROS #using_linux()
Parameters['human'] = {}
Parameters['human']['servo_percent'] = 49
Parameters['human']['motor_percent'] = 49
Parameters['network'] = {}
Parameters['network']['servo_percent'] = 49
Parameters['network']['motor_percent'] = 49
Parameters['IMU_SMOOTHING_PARAMETER'] = 0.99
Parameters['Hz'] = {}
Parameters['servo_pwm_null'] = 1450
Parameters['motor_pwm_null'] = Parameters['servo_pwm_null']
Parameters['servo_pwm_min'] = Parameters['servo_pwm_null']
Parameters['servo_pwm_max'] = Parameters['servo_pwm_null']
Parameters['motor_pwm_min'] = Parameters['servo_pwm_null']
Parameters['motor_pwm_max'] = Parameters['servo_pwm_null']
Parameters['behavioral_mode_choice'] = 'direct'
#Parameters['agent_choice'] = 'human'
Parameters['place_choice'] = 'local'

if Parameters['car_name'] == 'Mr_Blue_Back':
	Parameters['servo_pwm_smooth_manual_offset'] = -30
	Parameters['camera_pwm_manual_offset'] = -500
	Parameters['servo_feedback_center'] = 214
	Parameters['servo_feedback_right'] = 140
	Parameters['servo_feedback_left'] = 294
else:
	Parameters['servo_pwm_smooth_manual_offset'] = 0
	Parameters['camera_pwm_manual_offset'] = 0	

Parameters['HUMAN_SMOOTHING_PARAMETER_1'] = 0.75
Parameters['USE_MSE'] = True
Parameters['USE_SIG'] = True
Parameters['USE_IMU'] = True

Parameters['pid_motor_slope'] = (60-49)/3.0
Parameters['pid_motor_gain'] = 0.05
Parameters['pid_encoder_max'] = 4.0
Parameters['pid_motor_encoder_max'] = 4.0
Parameters['pid_motor_delta_max']= 0.05
Parameters['pid_motor_percent_max']= 99
Parameters['pid_motor_percent_min']= 0
Parameters['pid_steer_gain']= 0.05
Parameters['pid_steer_delta_max']= 0.05
Parameters['pid_steer_steer_percent_max']= 99
Parameters['pid_steer_steer_percent_min'] = 0
Parameters['use_servo_feedback'] = 0

Parameters['button_delta'] = 50
Parameters['button_number'] = 0
Parameters['button_timer'] = Timer()
Parameters['time_since_button_4'] = Timer()
Parameters['servo_pwm_smooth'] = 1000
Parameters['motor_pwm_smooth'] = 1000
Parameters['selector_mode'] = False
Parameters['encoder_smooth'] = 0.0
Parameters['network']['camera_percent'] = 49
Parameters['Hz']['mse'] = 0
Parameters['calibrated'] = False
Parameters['acc'] = {}
Parameters['gyro'] = {}
Parameters['head'] = {}


flex_names = []
for fb in ['f','b']:
    for lr in ['l','r','c']:
        for i in [0,1]:
            flex_names.append(d2n('x',fb,lr,i))
flex_names.append('xan0')

for f in flex_names:
    Parameters[f] = {}

Parameters['to_expose'] = [
	'IMU_SMOOTHING_PARAMETER',
	'behavioral_mode_choice',
	'agent_choice',
	'place_choice',
	'servo_pwm_smooth_manual_offset',
	'camera_pwm_manual_offset',
	'pid_motor_slope',
	'pid_motor_gain',
	'pid_encoder_max',
	'pid_motor_delta_max',
	'pid_motor_percent_max',
	'pid_motor_percent_min',
]

Network = {}
if True:
	Network['ABORT'] = False
	Network['network_output_sample'] = 0 # >= 0, <= 9
	Network['network_steer_gain'] = 6.0
	Network['network_camera_gain'] = 2.0
	Network['network_motor_gain'] = 0.8
	Network['network_motor_offset'] = 0
	Network['network_servo_smoothing_parameter'] = 0.85
	Network['network_motor_smoothing_parameter'] = 0.75
	Network['network_camera_smoothing_parameter'] = 0.0
	Network['weight_file_path'] = opjh('pytorch_models','net_10Jun18_00h00m45s.SqueezeNet')
	Network['USE_NETWORK'] = True
	Network['GREY_OUT_TOP_OF_IMAGE'] = False
	Network['USE_LAST_IMAGE_ONLY'] = False
	Network['visualize_activations'] = False
if False:
	Network['ABORT'] = False
	Network['network_output_sample'] = 4 # >= 0, <= 9
	Network['network_steer_gain'] = 2.0
	Network['network_camera_gain'] = 2.0
	Network['network_motor_gain'] = 0.333
	Network['network_motor_offset'] = 0
	Network['network_servo_smoothing_parameter'] = 0.95
	Network['network_motor_smoothing_parameter'] = 0.75
	Network['network_camera_smoothing_parameter'] = 0.75
	Network['weight_file_path'] = opjh('pytorch_models','net_10Jun18_00h00m45s.SqueezeNet')
	Network['USE_NETWORK'] = True
	Network['GREY_OUT_TOP_OF_IMAGE'] = False
	Network['USE_LAST_IMAGE_ONLY'] = True
	Network['visualize_activations'] = False
	#Network['motor_reverse_threshold'] = 64

Network['to_expose'] = [
	'network_output_sample',
	'network_steer_gain',
	'network_camera_gain',
	'network_motor_gain',
	'network_motor_offset',
	'network_servo_smoothing_parameter',
	'network_motor_smoothing_parameter',
	'network_camera_smoothing_parameter',
	'USE_LAST_IMAGE_ONLY',
]

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



"""




