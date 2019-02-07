#!/usr/bin/env python
from kzpy3.utils3 import *
import torch
import rospy
import std_msgs.msg
exec(identify_file_str)


def human_agent_callback(msg):
    N['mode']['human_agent'] = msg.data

def drive_mode_callback(msg):
    N['mode']['drive_mode'] = msg.data
    
def behavioral_mode_callback(msg):
    N['mode']['behavioral_mode'] = msg.data

bcs = '/bair_car'

rospy.Subscriber(
    bcs+'/human_agent',
    std_msgs.msg.Int32,
    callback=human_agent_callback)

rospy.Subscriber(
    bcs+'/behavioral_mode',
    std_msgs.msg.String,
    callback=behavioral_mode_callback)

rospy.Subscriber(
    bcs+'/drive_mode',
    std_msgs.msg.Int32,
    callback=drive_mode_callback)

N['pub'] = {}

N['pub']['control/camera'] = rospy.Publisher(
    'control/camera',std_msgs.msg.Int32,queue_size=5)

N['pub']['control/steer'] = rospy.Publisher(
    'control/steer',std_msgs.msg.Int32,queue_size=5)

N['pub']['control/motor'] = rospy.Publisher(
    'control/motor',std_msgs.msg.Int32,queue_size=5)

########################################################################
#  flex ROS
N['flex_motor'] = 49
N['flex_steer'] = 49

def flex_motor__callback(msg):
    N['flex_motor'] = msg.data

def flex_steer__callback(msg):
    N['flex_steer'] = msg.data

if N['use flex']:
    rospy.Subscriber('/bair_car/cmd/flex_motor', std_msgs.msg.Int32, callback=flex_motor__callback)
    rospy.Subscriber('/bair_car/cmd/flex_steer', std_msgs.msg.Int32, callback=flex_steer__callback)
#
########################################################################



    ########################################################################
    #  flex ROS
    N['flex_motor'] = 49
    N['flex_steer'] = 49

    def flex_motor__callback(msg):
        N['flex_motor'] = msg.data

    def flex_steer__callback(msg):
        N['flex_steer'] = msg.data

    if N['use flex']:
        rospy.Subscriber('/bair_car/cmd/flex_motor', std_msgs.msg.Int32, callback=flex_motor__callback)
        rospy.Subscriber('/bair_car/cmd/flex_steer', std_msgs.msg.Int32, callback=flex_steer__callback)
    #
    ########################################################################


def get_adjusted_commands(torch_camera,torch_steer,torch_motor,N):

    sm = N['network_motor_smoothing_parameter']

    if torch_motor >= 49:
        if N['mode']['behavioral_mode'] == 'direct':
            gm = N['network_motor_gain_direct']
        else:
            gm = N['network_motor_gain']
    else:
        gm = N['network_reverse_motor_gain']

    if N['mode']['behavioral_mode'] == 'direct':
        ss = N['network_servo_smoothing_parameter_direct']
        gs = N['network_steer_gain_direct']
        gc = N['network_camera_gain_direct']          
        sc = N['network_camera_smoothing_parameter_direct']
    else:
        ss = N['network_servo_smoothing_parameter']
        gs = N['network_steer_gain']
        gc = N['network_camera_gain']          
        sc = N['network_camera_smoothing_parameter']


    N['current']['camera'] = (1.0-sc)*torch_camera + sc*N['current']['camera']
    N['current']['steer'] = (1.0-ss)*torch_steer + ss*N['current']['steer']
    N['current']['motor'] = (1.0-sm)*torch_motor + sm*N['current']['motor']

    adjusted_motor = int(gm*(N['current']['motor']-49) + N['network_motor_offset'] + 49)
    adjusted_steer = int(gs*(N['current']['steer']-49) + 49)
    adjusted_camera = int(gc*(N['current']['camera']-49) + 49)

    adjusted_motor = bound_value(adjusted_motor,0,99)
    adjusted_steer = bound_value(adjusted_steer,0,99)
    adjusted_camera = bound_value(adjusted_camera,0,99)

    adjusted_motor = min(adjusted_motor,N['max motor'])
    adjusted_motor = max(adjusted_motor,N['min motor'])

    return adjusted_camera,adjusted_steer,adjusted_motor
#EOF
