from kzpy3.utils2 import *
from kzpy3.Menu_app.menu import *

menu_path = opjh('.menu','network_node')

Topics = [
    ('network_smoothing_parameter',0.75,Float),
    ('network_output_sample',4,Int),
    ('network_motor_offset',3,Int),
    ('network_steer_gain',8.1,Float),
    ('network_motor_gain',1.4,Float),
    ('servo_pwm_smooth_manual_offset',169,Int)
]

if __name__ == '__main__':
    menu(Topics,menu_path)
#EOF