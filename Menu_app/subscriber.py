from kzpy3.utils2 import *
from kzpy3.Menu_app.ros_strings import *


Topics = [
    ('network_smoothing_parameter',Float),
    ('network_output_sample',Int),
    ('network_motor_offset',Int),
    ('network_steer_gain',Float),
    ('network_motor_gain',Float),
    ('servo_pwm_smooth_manual_offset',Int)
]

subscription_strs = get_ros_subscriber_strs(Topics)

for c in [rosimport_str,rospyinit_str]+subscription_strs:
    if using_linux(): exec(c)
raw_enter()


#EOF
