#!/usr/bin/env python
from kzpy3.vis3 import *
import rospy
import torch
import std_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Image
import kzpy3.Menu_app.menu2 as menu2
import cv2

if '__file__' not in locals() or __file__ == 'INTERPRETER': 
    import kzpy3.Cars.n26Dec18.nodes.Activity_Module as Activity_Module
    import kzpy3.Cars.n26Dec18.nodes.default_values as default_values
    import kzpy3.Cars.n26Dec18.nodes.network_utils.net_utils
    Arguments['desktop_mode']=True
else:
    import network_utils.net_utils
    import Activity_Module
    import default_values

exec(identify_file_str)

try:
    if Arguments['desktop_mode']:
        raw_enter("Arguments['desktop mode'] == True ")
except:
    Arguments = {}
    Arguments['desktop_mode'] = False


N = default_values.P
for k in ['current','torch','timer','mode','net']:
    N[k] = {}

N['current']['camera'] = 49
N['current']['steer'] = 49
N['current']['motor'] = 49

N['torch']['camera'] = 49
N['torch']['steer'] = 49
N['torch']['motor'] = 49

N['timer']['parameter_file_load'] = Timer(2)
N['timer']['waiting'] = Timer(1)
N['timer']['frequency'] = Timer(5)
N['timer']['show'] = Timer(0.25)
N['timer']['print'] = Timer(0.5)

N['mode']['human_agent'] = 1
N['mode']['behavioral_mode'] = 'direct'
N['mode']['drive_mode'] = 1

N['net']['Torch_network'] = None
N['net']['loaded_net'] = False


def human_agent_callback(msg):
    N['mode']['human_agent'] = msg.data

def drive_mode_callback(msg):
    N['mode']['drive_mode'] = msg.data
    
def behavioral_mode_callback(msg):
    N['mode']['behavioral_mode'] = msg.data

N['bcs'] = ''
for t in rospy.get_published_topics():
    if '/bair_car/zed' in t[0]:
        N['bcs'] = '/bair_car'
        break

rospy.Subscriber(N['bcs']+'/human_agent', std_msgs.msg.Int32, callback=human_agent_callback)
rospy.Subscriber(N['bcs']+'/behavioral_mode', std_msgs.msg.String, callback=behavioral_mode_callback)
rospy.Subscriber(N['bcs']+'/drive_mode', std_msgs.msg.Int32, callback=drive_mode_callback)

N['pub'] = {}
N['pub']['cmd/camera'] = rospy.Publisher('cmd/camera',std_msgs.msg.Int32,queue_size=5)
N['pub']['cmd/steer'] = rospy.Publisher('cmd/steer',std_msgs.msg.Int32,queue_size=5)
N['pub']['cmd/motor'] = rospy.Publisher('cmd/motor',std_msgs.msg.Int32,queue_size=5)

rospy.init_node('network_node',anonymous=True,disable_signals=True)


if __name__ == '1__main__':

    N['ABORT'] = False

    while not rospy.is_shutdown() and N['ABORT'] == False:

        for i in range(4):
            step()

        if N['net']['Torch_network'] != None:
            pass
            """
            if 'solver' in Torch_network:
                if len(Torch_network['solver'].A.keys()) > 0:
                    show_color_net_inputs(
                        Torch_network['solver'].A['camera_input'],
                        Torch_network['solver'].A['pre_metadata_features_metadata'])
                    raw_enter()
            """

#EOF

    