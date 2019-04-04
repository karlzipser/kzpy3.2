#!/usr/bin/env python
from kzpy3.utils3 import *
import torch
#import torch.nn
#import torch.autograd
import rospy
import std_msgs.msg
#import geometry_msgs.msg
from std_msgs.msg import Int32MultiArray
#from sensor_msgs.msg import Image
exec(identify_file_str)


def ros_init(N):

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
        #print N['mode']['behavioral_mode']

    bcs = '/bair_car'

    rospy.Subscriber(
        bcs+'/human_agent',
        std_msgs.msg.Int32,
        callback=human_agent_callback)

    rospy.Subscriber(
        '/behavioral_mode',
        std_msgs.msg.String,
        callback=behavioral_mode_callback)

    rospy.Subscriber(
        bcs+'/drive_mode',
        std_msgs.msg.Int32,
        callback=drive_mode_callback)

    N['pub'] = {}

    N['pub']['net/steer'] = rospy.Publisher(
        'net/steer',std_msgs.msg.Float32,queue_size=5)

    N['pub']['net/motor'] = rospy.Publisher(
        'net/motor',std_msgs.msg.Float32,queue_size=5)


    N['pub']['net/encoder0'] = rospy.Publisher('encoder0',Int32MultiArray,queue_size = 10)
    N['pub']['net/encoder1'] = rospy.Publisher('encoder1',Int32MultiArray,queue_size = 10)
    N['pub']['net/encoder2'] = rospy.Publisher('encoder2',Int32MultiArray,queue_size = 10)

    N['pub']['net/header0'] = rospy.Publisher('header0',Int32MultiArray,queue_size = 10)
    N['pub']['net/header1'] = rospy.Publisher('header1',Int32MultiArray,queue_size = 10)
    N['pub']['net/header2'] = rospy.Publisher('header2',Int32MultiArray,queue_size = 10)

    N['pub']['net/motor0'] = rospy.Publisher('motor0',Int32MultiArray,queue_size = 10)
    N['pub']['net/motor1'] = rospy.Publisher('motor1',Int32MultiArray,queue_size = 10)
    N['pub']['net/motor2'] = rospy.Publisher('motor2',Int32MultiArray,queue_size = 10)

def metadata_init(N):
    """Making metadata tensors in advance so they 
need not be constructed during runtime.
For SqueezeNet40 models."""
    TP = {}
    TP['behavioral_modes_no_heading_pause'] = \
        ['direct','follow','furtive','play','left','right']
    # note, 'center' is not included in
    # TP['behavioral_modes_no_heading_pause']
    # because 'center' is converted to 'direct' below.
    TP['behavioral_modes'] = \
        TP['behavioral_modes_no_heading_pause']+['heading_pause']
    # Order must stay the same to be compatible with network.

    Metadata_tensors = {}
    cm(5)
    for the_behaviorial_mode in TP['behavioral_modes']:

        metadata = torch.FloatTensor(1,128,23,41).cuda()

        typical_encoder_value = 3.0

        metadata[0,0,:,:] = typical_encoder_value / 100.0 / 5.0

        for x in range(41):
            metadata[0,1,:,x] = (1.0-x/41.0)

        for x in range(41):
            metadata[:,2,:,x] = x/41.0

        for x in range(23):
            metadata[0,3,x,:] = (1.0-x/23.0)

        for x in range(23):
            metadata[0,4,x,:] = x/23.0

        mode_ctr = 1

        for b in TP['behavioral_modes']:
            if b == the_behaviorial_mode:
                metadata[0,-mode_ctr,:,:] = 1.0; mode_ctr += 1
            else:
                metadata[0,-mode_ctr,:,:] = 0.0; mode_ctr += 1

        Metadata_tensors[the_behaviorial_mode] = metadata
        cm(103)
        
    N['behavioral_metadatas'] = Metadata_tensors



#EOF
