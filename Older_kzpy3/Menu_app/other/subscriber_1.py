from kzpy3.utils3 import *
from kzpy3.Menu_app.ros_strings import *

Topics = [
    ('/bair_car/steer',Int),
    ('/bair_car/motor',Int),
]
output_file = opjD('temp1.py')


dic_name = 'P'

a = ros_start_strs = get_ros_start_strs(node_name)
b = subscription_strs = get_ros_subscriber_strs(Topics,dic_name)
c = get_ros_publisher_strs(Topics)

d = a+b+c

list_of_strings_to_txt_file(output_file,d)
CS(d2s("Wrote ROS code to",output_file))

if HAVE_ROS:
    for e in d:
        exec(e)
else:
    CS("Don't have ROS.")



#EOF
