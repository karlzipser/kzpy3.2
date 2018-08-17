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

pprint(subscription_strs)

list_of_strings_to_txt_file(opjh('temp_.py'),[rosimport_str,rospyinit_str]+subscription_strs)
raw_enter()
from temp_ import *

#EOF
