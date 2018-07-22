#!/usr/bin/env python
"""
reed to run roslaunch first, e.g.,

roslaunch bair_car bair_car.launch use_zed:=true record:=false
"""

from kzpy3.utils2 import *
import default_values
N = {}
for k in default_values.Network.keys():
    N[k] = default_values.Network[k]
if not N['USE_NETWORK']:
    spd2s('network_node.py::not using network')
    time.sleep(3600*24)
    assert(False)
import net_utils
########################################################
#          ROSPY SETUP SECTION
import roslib
import std_msgs.msg
import geometry_msgs.msg
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
bridge = CvBridge()

rospy.init_node('listener',anonymous=True)

left_list = []
right_list = []
nframes = 2 #figure out how to get this from network



human_agent = 1
behavioral_mode = 'direct'
drive_mode = 0
direct = 0.0
follow = 0.0
furtive = 0.0
play = 0.0
left = 0.0
right = 0.0
current_steer = 49
current_motor = 49
    
def right_callback(data):
    global left_list, right_list, solver
    cimg = bridge.imgmsg_to_cv2(data,"bgr8")
    if len(right_list) > nframes + 3:
        right_list = right_list[-(nframes + 3):]
    right_list.append(cimg)
def left_callback(data):
    global left_list, right_list
    cimg = bridge.imgmsg_to_cv2(data,"bgr8")
    if len(left_list) > nframes + 3:
        left_list = left_list[-(nframes + 3):]
    left_list.append(cimg)
def human_agent_callback(msg):
    global human_agent
    human_agent = msg.data
def drive_mode_callback(msg):
    global drive_mode
    drive_mode = msg.data
def behavioral_mode_callback(msg):
    global behavioral_mode, direct, follow, furtive, play
    behavioral_mode = msg.data
    direct = 0.0
    follow = 0.0
    furtive = 0.0
    play = 0.0
    if behavioral_mode == 'direct':
        direct = 1.0
    elif behavioral_mode == 'follow':
        follow = 1.0
    elif behavioral_mode == 'furtive':
        furtive = 1.0
    elif behavioral_mode == 'play':
        play = 1.0

def button_number_callback(msg):
    global left,right
    button_number = msg.data
    left = 0.0
    right = 0.0
    if button_number == 3:
        right = 1.0
    elif button_number == 1:
        left = 1.0


def network_weights_name_callback(msg):
    s = msg.data
    if s != N['weight_file_path']:
        N['weight_file_path'] = s
        N['RELOAD_NET'] = True
    else:
        N['RELOAD_NET'] = False


def callback_network_output_sample(msg):
    N['network_output_sample'] = msg.data
def callback_network_motor_offset(msg):
    N['network_motor_offset'] = msg.data
def callback_network_steer_gain(msg):
    N['network_steer_gain'] = msg.data
def callback_network_motor_gain(msg):
    N['network_motor_gain'] = msg.data
def callback_network_smoothing_parameter(msg):
    N['network_smoothing_parameter'] = msg.data


steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=100)
motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=100)
Hz_network_pub = rospy.Publisher('Hz_network', std_msgs.msg.Float32, queue_size=5)
rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)
rospy.Subscriber('/bair_car/human_agent', std_msgs.msg.Int32, callback=human_agent_callback)
rospy.Subscriber('/bair_car/behavioral_mode', std_msgs.msg.String, callback=behavioral_mode_callback)
rospy.Subscriber('/bair_car/network_weights_name', std_msgs.msg.String, callback=network_weights_name_callback)
rospy.Subscriber('/bair_car/drive_mode', std_msgs.msg.Int32, callback=drive_mode_callback)
rospy.Subscriber('/bair_car/button_number', std_msgs.msg.Int32, callback=button_number_callback)
rospy.Subscriber('/network_output_sample', std_msgs.msg.Int32, callback=callback_network_output_sample)
rospy.Subscriber('/network_motor_offset', std_msgs.msg.Int32, callback=callback_network_motor_offset)
rospy.Subscriber('/network_steer_gain', std_msgs.msg.Float32, callback=callback_network_steer_gain)
rospy.Subscriber('/network_motor_gain', std_msgs.msg.Float32, callback=callback_network_motor_gain)
rospy.Subscriber('/network_smoothing_parameter', std_msgs.msg.Float32, callback=callback_network_smoothing_parameter)



N['RELOAD_NET'] = True
frequency_timer = Timer(1.0)
print_timer = Timer(5)

Hz = 0


low_frequency_pub_timer = Timer(0.5)
low_frequency_pub_timer2 = Timer(5)

#Torch_network = net_utils.Torch_Network(N)


while True:
    if N['RELOAD_NET']: # temporary experiment
        N['RELOAD_NET'] = False
        Torch_network = net_utils.Torch_Network(N)

    time.sleep(0.001)
    #print_timer.message(d2s("N['network_steer_gain'] =",N['network_steer_gain']))#######
    Hz = frequency_timer.freq(name='Hz_network',do_print=False)
    if is_number(Hz):
        if low_frequency_pub_timer.check():
            Hz_network_pub.publish(std_msgs.msg.Float32(Hz))
            low_frequency_pub_timer.reset()

    s = N['network_smoothing_parameter']

    #print_timer.message(d2s('network_node::drive_mode =',drive_mode))#######

    if human_agent == 0 and drive_mode == 1:
        if len(left_list) > nframes + 2:
            camera_data = Torch_network['format_camera_data'](left_list,right_list)
            metadata = Torch_network['format_metadata']((right,left,play,furtive,follow,direct))
            torch_motor, torch_steer = Torch_network['run_model'](camera_data, metadata, N)

            if 'Do smoothing of percents...':
                current_steer = (1.0-s)*torch_steer + s*current_steer
                current_motor = (1.0-s)*torch_motor + s*current_motor

            adjusted_motor = N['network_motor_gain']*(current_motor-49) + N['network_motor_offset'] + 49
            adjusted_steer = N['network_steer_gain']*(current_steer-49) + 49

            adjusted_motor = bound_value(adjusted_motor,0,99)
            adjusted_steer = bound_value(adjusted_steer,0,99)

            steer_cmd_pub.publish(std_msgs.msg.Int32(adjusted_steer))
            motor_cmd_pub.publish(std_msgs.msg.Int32(adjusted_motor))

        if low_frequency_pub_timer2.check():
            pd2s("N['weight_file_path'] =",N['weight_file_path'])
            #spd2s(adjusted_steer,adjusted_motor,drive_mode, human_agent, behavioral_mode)
            low_frequency_pub_timer2.reset()
    else:
        #print 'network paused'
        time.sleep(0.1)

print 'goodbye!'
print "unix(opjh('kzpy3/kill_ros.sh'))"
unix(opjh('kzpy3/kill_ros.sh'))


#EOF

    