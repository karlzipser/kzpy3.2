from kzpy3.utils3 import *
exec(identify_file_str)

P = {}
_ = P
_['project_path'] = pname(__file__)
print _['project_path']

_['agent_is_human'] = False


_['stopped_timer'] = Timer()
_['stopped'] = False
_['stay_stopped'] = False
_['stopped_time_min'] = 0.5


_['MOCK_ARDUINO_VERSION'] = False # Note, unrelated to 'desktop_mode' command line arg
_['MOCK_ARDUINO_VERSION/run_name'] = 'tegra-ubuntu_16Nov18_13h02m06s'
_['MOCK_ARDUINO_VERSION/h5py_path'] = opjm('/home/karlzipser/Desktop/Data/2_TB_Samsung_n3/rosbags__preprocessed_data/tu_15to16Nov2018/locations/local/left_direct_stop/h5py')
_['MOCK_ARDUINO_VERSION/nvidia_run_name'] = _['MOCK_ARDUINO_VERSION/run_name']
_['MOCK_ARDUINO_VERSION/nvidia_h5py_path'] = _['MOCK_ARDUINO_VERSION/h5py_path']

_['desktop version/artifical mode'] = False
_['desktop version/pwm to screen'] = True

_['customers'] = ['Arduino','Network','Weights','Flex','Control',]
_['drive_mode'] = 0
_['use lights'] = True
_['now in calibration mode'] = False

_['USE_MSE'] = True
_['USE_IMU'] = True
_['USE_ROS'] = HAVE_ROS

_['d_heading_for_end_turning'] = 60
_['max motor'] = 60
_['min motor'] = 27
_['motor backward max'] = 40
_['motor forward min'] = 52
_['arduino print'] = True
_['network print'] = True
_['control print'] = True
_['flex print'] = True
############# NETWORK PARAMETERS
_['ldr_gain'] = 0.1
_['backup parameter'] = 1/3. #-0.1 #0.5
_['network_output_sample'] = 0 # >= 0, <= 9
_['network_steer_gain'] = 2.0
_['network_camera_gain'] = 4.0
_['network_motor_gain'] = 0.8
_['from still motor offset gain'] = 0.0
_['low velocity direct steer gain'] = 4.0
_['network_reverse_motor_gain'] = 2.
_['network_motor_offset'] = 0
_['network_reverse_motor_offset'] = -5
_['network_servo_smoothing_parameter'] = 0.85
_['network_motor_smoothing_parameter'] = 0.95
_['network_camera_smoothing_parameter'] = 0.75
_['network_servo_smoothing_parameter_direct'] = 0.85
_['network_steer_gain_direct'] = 1.5
_['network_camera_gain_direct'] = 0.5         
_['network_motor_gain_direct'] = 1.
_['USE_NETWORK'] = True
_['GREY_OUT_TOP_OF_IMAGE'] = False 
_['USE_LAST_IMAGE_ONLY'] = False
_['visualize_activations'] = False
_['camera_move_threshold'] = 0
_['camera_auto_zero_for_small_values_int'] = 0
_['saccade timer parameter'] = 1.0
_['ldr_on_time'] = 0.25
_['ldr_off_time'] = 0.25
#_['cmd_camera_to_camera_heading_cooeficient'] = 0. #0.75
_['temp_camera'] = 49
_['still_motor_offset_gain'] = 0.0
###########################
_['use flex'] = True ####TEMP_CHANGE
_['flex_motor_smoothing_parameter'] = _['network_motor_smoothing_parameter']
_['flex_servo_smoothing_parameter'] = _['network_servo_smoothing_parameter']
_['flex_motor_gain'] = 1.5
_['flex_steer_gain'] = _['network_steer_gain']
_['flex_network_output_sample'] = 0
_['flex max motor'] = _['max motor']
_['flex min motor'] = _['min motor']
_['flex/motor collision threshold'] = 40
_['flex/motor white light threshold'] = 45

_['show_net_input'] = False
_['show_net_activity'] = False
_['menu name'] = 'arduino menu'
_['cmd/autostart menu'] = False
_['cmd/clear_screen'] = False
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
_['CALIBRATION_NULL_START_TIME'] = 0.0
_['CALIBRATION_START_TIME'] = 1.0
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

_['servo_pwm_smooth'] = 1000
_['motor_pwm_smooth'] = 1000

_['servo_pwm_smooth_manual_offset'] = 0

_['camera_pwm_manual_offset'] = 133

_['HUMAN_SMOOTHING_PARAMETER_1'] = 0.75

_['use_net_motor_PID'] = True
_['use_human_motor_PID'] = False
_['human_PID_motor_percent'] = 53
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

_['button_delta'] = 50
_['button_number'] = 0
_['button_timer'] = Timer()

_['encoder_smooth'] = 0.0
_['encoder'] = 0.0
_['network']['camera_percent'] = 49
_['Hz']['mse'] = 0
_['acc'] = {}
_['gyro'] = {}
_['head'] = {}
_['autostart menu'] = False
_['desktop version/start index'] = 5000
_['delta servo_pwm for calibration'] = 900
_['delta motor_pwm for calibration'] = 800
_['Arduinos'] = {}
def _fun_light(num):
	try:
	    if 'LIGHTS' in _['Arduinos']:
	        _['Arduinos']['LIGHTS'].write(d2n(""" "(""",num,""")" """))
	except:
		print('_fun_light(num) lights write failed.')
        #cy('light signal',num)
_['light'] = _fun_light
_['Lights'] = {
    'left right red'    :62,
    'left right red, left blink yellow' :61,
    'left right red, right blink yellow'    :63,
    'left right blink yellow' :64,
    'blue'  :5,
    'white' :7,
    'green' :6,
    'purple'    :118,
    'purple blink'    :120,
    'blue off'  :115,
    'white off' :117,
    'green off' :116,
    'purple off'    :119,
    'lights out'    :22,
    'lights enabled'    :21,
}
_['lights/human, YES'] = 		'100'
_['lights/human, NO'] = 			'101'
_['net_hide_colors'] = ['magenta']

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
    _[f+'/gain'] = 1.0

for f in flex_names:
    _[f] = {}

_['to_hide'] = []
_['To Expose'] = {}
_['To Expose']['Arduino'] = [
	'ABORT',
	'agent_is_human',
	'servo_pwm_smooth_manual_offset',
	'camera_pwm_manual_offset',
	'use_human_motor_PID',
	'human_PID_motor_percent',
	'now in calibration mode',
	'desktop version/pwm to screen',
	'delta servo_pwm for calibration',
	'delta motor_pwm for calibration',
    'd_heading_for_end_turning',
    'arduino print',
    'network print',
    'control print',
    'flex print',
    'max motor',
    'min motor',
    'motor backward max',
    'motor forward min',
    'stopped_time_min',
]
_['To Expose']['Network'] = [
    'ABORT',
    'backup parameter',
    'still_motor_offset_gain',
	'network_output_sample',
	'network_steer_gain',
	'network_camera_gain',
	'network_camera_gain_direct',
	'network_motor_gain',
	'network_motor_gain_direct',
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
	'network_reverse_motor_gain',
	'net_hide_colors',
	'network_servo_smoothing_parameter_direct',
	'network_steer_gain_direct',
	'low velocity direct steer gain',
    'ldr_gain',
    'use_net_motor_PID',
    #'cmd_camera_to_camera_heading_cooeficient',
    'temp_camera',
    'saccade timer parameter',
    'ldr_on_time',
    'ldr_off_time',
]
_['To Expose']['Control'] = [
    'ABORT',
]
_['To Expose']['Flex'] = [
    'ABORT',
	'flex_motor_smoothing_parameter',
	'flex_servo_smoothing_parameter',
	'flex_motor_gain',
	'flex_steer_gain',
    'flex_network_output_sample',
    'flex min motor',
    'flex max motor',
    'flex_graphics',
	'flex/motor collision threshold',
	'flex/motor white light threshold',
]
for f in flex_names:
    _['To Expose']['Flex'].append(f+'/gain')

_['flex_graphics'] = False
if username == 'nvidia':
	_['weight_file_path'] = opjm("rosbags/Network_Weights")
else:
	_['weight_file_path'] = opjD('Network_Weights')

try:
	_['To Expose']['Weights'] = []
	_['weight_files'] = {}
	Model_folders = {}
	for f in sggo(_['weight_file_path'],'*'):

		weight_files = sort_dir_by_ctime(f)
		l = len(weight_files)
		n = d2n(fname(f)," (",l,")")
		_[n] = 0
		_['To Expose']['Weights'].append(n)
		_['weight_files'][n] = weight_files

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    CS_('Exception!',emphasis=True)
    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

_['LOAD NETWORK'] = False

_['modalities'] = ['headings','encoders','motors','steers']
_['topic_suffix'] = ''

#EOF