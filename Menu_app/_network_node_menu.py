from kzpy3.utils2 import *
from kzpy3.Menu_app.menu import *

Arguments = {}
for a in Args.keys():
	ar = Args[a]
	if str_is_int(ar):
		Arguments[a] = int(ar)
	else:
		Arguments[a] = ar

menu = False
if Arguments['NODE'] == 'network':
	menu_path = opjh('.menu','network_node')
	Topics = [
		('network_output_sample',4,Int), # >= 0, <= 9
		('network_steer_gain',1.0,Float),
		('network_camera_gain',1.0,Float,
		('network_motor_gain',1.0,Float),
		('network_motor_offset',0,Float),
		('network_smoothing_parameter',0.75,Float),
		('network_servo_smoothing_parameter',.75,Float)
	]
elif Arguments['NODE'] == 'arduino'
	menu_path = opjh('.menu','arduino_node')
	Topics = [
	    ('servo_feedback_left',193,Int),
	    ('servo_feedback_right',358,Int),
	    ('servo_feedback_center',270,Int),
	    ('servo_pwm_smooth_manual_offset',200,Int),
	    ('camera_pwm_manual_offset',-450,Int)
	]

if __name__ == '__main__':
	if menu_path:
	    menu(Topics,menu_path)
	else:
		print('Invalid argument '+Arguments['NODE'])
		
#EOF
