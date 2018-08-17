from kzpy3.utils2 import *
from kzpy3.Menu_app.menu import *

menu_path = opjh('.menu','arduino_node')

Topics = [
    ('servo_feedback_left',0,Int),
    ('servo_feedback_right',0,Int),
    ('servo_feedback_center',0,Int),
    ('servo_pwm_smooth_manual_offset',50,Int)
    ('camera_pwm_manual_offset',0,Int)
]

if __name__ == '__main__':
    menu(Topics,menu_path)

#EOF