from kzpy3.utils2 import *
from kzpy3.Menu_app.ros_strings import *


Topics = [
    ('/bair_car/servo_feedback',Float),
    ('/bair_car/motor',Int),
]

subscription_strs = get_ros_subscriber_strs(Topics)

for c in [rosimport_str,rospyinit_str]+subscription_strs:
    if using_linux(): exec(c)


for i in range(1000):
    print R

raw_enter()


#EOF
