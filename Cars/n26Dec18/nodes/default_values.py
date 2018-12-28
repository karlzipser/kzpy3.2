from kzpy3.utils3 import *
exec(identify_file_str)

P = {}
_ = P
_['agent_is_human'] = True
_['use_motor_PID'] = True
_['desktop version'] = True
if _['desktop version']:
	_['bcs'] = ''
else:
	_['bcs'] = '/bair_car'

_['customers'] = ['Arduino','Network','Weights','Flex']
_['drive_mode'] = 0
_['use sound'] = True
_['now in calibration mode'] = False
_['use flex'] = False
_['USE_MSE'] = True
_['USE_IMU'] = True
_['USE_ROS'] = HAVE_ROS # using_linux()
_['human_PID_motor_percent'] = 53
_['max motor'] = 63
_['min motor'] = 0#49-(63-49)
_['show_net_input'] = False
_['show_net_activity'] = False
_['menu name'] = 'arduino menu'
_['cmd/autostart menu'] = False
_['cmd/clear_screen'] = False
#_['use menu'] = True
_['print_timer time'] = 0.1
_['IMU/print_timer'] = Timer(_['print_timer time'])
_['MSE/print_timer'] = Timer(_['print_timer time'])
_['car_name'] = os.environ["COMPUTER_NAME"]
_['calibrated'] = False
_['ABORT'] = False
_['servo_percent'] = 49
_['motor_percent'] = 49
_['cmd/camera'] = 49
_['cmd/steer'] = 49
_['cmd/motor'] = 49
_['LED_number'] = {}
_['LED_number']['current'] = 0
_['CALIBRATION_NULL_START_TIME'] = 3.0
_['CALIBRATION_START_TIME'] = 4.0
_['human'] = {}
_['human']['servo_percent'] = 49
_['human']['motor_percent'] = 49
_['network'] = {}
_['network']['servo_percent'] = 49
_['network']['motor_percent'] = 49
_['IMU_SMOOTHING_PARAMETER'] = 0.95
_['Hz'] = {}
_['servo_pwm_null'] = 1450
_['motor_pwm_null'] = _['servo_pwm_null']
_['servo_pwm_min'] = _['servo_pwm_null']
_['servo_pwm_max'] = _['servo_pwm_null']
_['motor_pwm_min'] = _['servo_pwm_null']
_['motor_pwm_max'] = _['servo_pwm_null']
#_['behavioral_mode_choice'] = 'direct'
#_['place_choice'] = 'local'
_['servo_pwm_smooth_manual_offset'] = 0
_['camera_pwm_manual_offset'] = 0	
_['HUMAN_SMOOTHING_PARAMETER_1'] = 0.75

_['pid_motor_slope'] = (60-49)/3.0
_['pid_motor_gain'] = 0.05
_['pid_encoder_max'] = 4.0
_['pid_motor_encoder_max'] = 4.0
_['pid_motor_delta_max']= 0.05
_['pid_motor_percent_max']= 99
_['pid_motor_percent_min']= 0
_['pid_steer_gain']= 0.05
_['pid_steer_delta_max']= 0.05
_['pid_steer_steer_percent_max']= 99
_['pid_steer_steer_percent_min'] = 0
#_['use_servo_feedback'] = 0
_['button_delta'] = 50
_['button_number'] = 0
_['button_timer'] = Timer()
_['servo_pwm_smooth'] = 1000
_['motor_pwm_smooth'] = 1000
_['encoder_smooth'] = 0.0
_['encoder'] = 0.0
_['network']['camera_percent'] = 49
_['Hz']['mse'] = 0
_['acc'] = {}
_['gyro'] = {}
_['head'] = {}
_['autostart menu'] = False
_['desktop version/start index'] = 5000

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
    _[f] = {}
_['to_hide'] = []

_['To Expose'] = {}
_['To Expose']['Arduino'] = [
	'ABORT',
	#'behavioral_mode_choice',
	'agent_is_human',
	#'place_choice',
	'servo_pwm_smooth_manual_offset',
	'camera_pwm_manual_offset',
	#'use LIDAR',
	'use sound',
	'use_motor_PID',
	'desktop version',
	'human_PID_motor_percent',
]

_['To Expose']['Network'] = [
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
	'min motor',
	'show_net_input',
	'show_net_activity',
	'camera_move_threshold',
	'camera_auto_zero_for_small_values_int',
	'network_reverse_motor_gain',
	'desktop version',
]

_['To Expose']['Flex'] = [
	'flex_motor_smoothing_parameter',
	'flex_servo_smoothing_parameter',
	'flex_motor_gain',
	'flex_steer_gain',
]

def sort_dir_by_ctime(dir_path):
	#print dir_path
	#raw_enter()
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
	    paths.append(path)
	return paths

if username == 'nvidia':
	_['weight_file_path'] = opjm("rosbags/networks") #opjh('pytorch_models/epoch6goodnet')
else:
	_['weight_file_path'] = opjD('Networks/_net_15Sept2018_1Nov_with_reverse_')
	#cr("_['weight_file_path'] =",_['weight_file_path'])

try:
	#cr(1)
	_['To Expose']['Weights'] = []
	_['weight_files'] = {}
	Model_folders = {}
	#cr(2)
	for f in sggo(_['weight_file_path'],'*'):
		#cr(3)
		#print f
		weight_files = sort_dir_by_ctime(f)
		l = len(weight_files)
		n = d2n(fname(f)," (",l,")")
		_[n] = [False]
		_['To Expose']['Weights'].append(n)
		_['weight_files'][n] = weight_files

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    CS_('Exception!',emphasis=True)
    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

_['LOAD NETWORK'] = False

############# NETWORK PARAMETERS
_['network_output_sample'] = 0 # >= 0, <= 9
_['network_steer_gain'] = 4.0
_['network_camera_gain'] = 8.0
_['network_motor_gain'] = 1.0
_['network_reverse_motor_gain'] = 1.5
_['network_motor_offset'] = 0
_['network_servo_smoothing_parameter'] = 0.85
_['network_motor_smoothing_parameter'] = 0.85
_['network_camera_smoothing_parameter'] = 0.0
_['USE_NETWORK'] = True
_['GREY_OUT_TOP_OF_IMAGE'] = False
_['USE_LAST_IMAGE_ONLY'] = False
_['visualize_activations'] = False
_['flex_motor_smoothing_parameter'] = _['network_motor_smoothing_parameter']
_['flex_servo_smoothing_parameter'] = _['network_servo_smoothing_parameter']
_['flex_motor_gain'] = _['network_motor_gain']
_['flex_steer_gain'] = _['network_steer_gain']
_['camera_move_threshold'] = 0
_['camera_auto_zero_for_small_values_int'] = 0
###########################

#EOF