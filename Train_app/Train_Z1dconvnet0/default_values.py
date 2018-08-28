from kzpy3.utils3 import *
exec(identify_file_str)

P = {}
P['The menu path.'] = opjh('kzpy3/Train_app/Train_Z1dconvnet0/__local__/')
P['acc triggers'] = 'shutdown'
P['car_name'] = os.environ["COMPUTER_NAME"]
P['calibrated'] = False
P['ABORT'] = False
P['agent_choice'] = 'human'
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
P['USE_ROS'] = HAVE_ROS #using_linux()
P['human'] = {}
P['human']['servo_percent'] = 49
P['human']['motor_percent'] = 49
P['network'] = {}
P['network']['servo_percent'] = 49
P['network']['motor_percent'] = 49
P['IMU_SMOOTHING_PARAMETER'] = 0.99
P['servo_pwm_null'] = 1450
P['motor_pwm_null'] = P['servo_pwm_null']
P['servo_pwm_min'] = P['servo_pwm_null']
P['servo_pwm_max'] = P['servo_pwm_null']
P['motor_pwm_min'] = P['servo_pwm_null']
P['motor_pwm_max'] = P['servo_pwm_null']
P['behavioral_mode_choice'] = 'direct'
P['agent_choice'] = 'human'
P['place_choice'] = 'local'
P['button_delta'] = 50
P['button_number'] = 0
P['servo_pwm_smooth'] = 1000
P['motor_pwm_smooth'] = 1000
P['selector_mode'] = False
P['encoder_smooth'] = 0.0
P['network']['camera_percent'] = 49
P['calibrated'] = False
P['to_expose'] = []
P['to_hide'] = ['to_expose','to_hide','The menu path.']
for k in P.keys():
	if k not in P['to_hide']:
		P['to_expose'].append(k)


Network = {}
if True:
	Network['ABORT'] = False
	Network['network_output_sample'] = 4 # >= 0, <= 9
	Network['network_steer_gain'] = 8.0
	Network['network_camera_gain'] = 8.0
	Network['network_motor_gain'] = 1.0
	Network['network_motor_offset'] = 0
	Network['network_servo_smoothing_parameter'] = 0.95
	Network['network_motor_smoothing_parameter'] = 0.75
	Network['network_camera_smoothing_parameter'] = 0.75
	Network['weight_file_path'] = opjh('pytorch_models','net_10Jun18_00h00m45s.SqueezeNet')
	Network['USE_NETWORK'] = True
	Network['GREY_OUT_TOP_OF_IMAGE'] = False
	Network['USE_LAST_IMAGE_ONLY'] = True
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



