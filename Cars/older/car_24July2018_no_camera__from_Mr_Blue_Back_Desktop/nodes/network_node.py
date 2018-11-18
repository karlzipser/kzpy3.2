#!/usr/bin/env python
from kzpy3.utils3 import *
import Default_values.network.default_values
exec(identify_file_str)
import rospy

N = {}
for k in Default_values.network.default_values.Network.keys():
    N[k] = Default_values.network.default_values.Network[k]

"""
import kzpy3.Menu_app.menu
menu_path = N['The menu path.']
if not os.path.exists(menu_path):
    os.makedirs(menu_path)
try:
    os.remove(opj(path,'ready'))
except:
    passthreading.Thread(target=kzpy3.Menu_app.menu.load_menu_data,args=[menu_path,N]).start()
"""

if not N['USE_NETWORK']:
    spd2s('network_node.py::not using network')
    time.sleep(3600*24)
    assert(False)

import net_utils

import roslib
import std_msgs.msg
import geometry_msgs.msg
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
bridge = CvBridge()

rospy.init_node('network_node',anonymous=True,disable_signals=True)

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
center = 0.0
button_number_previous = -9999
button_timer = Timer()
current_camera = 49
current_steer = 49
current_motor = 49
button_just_changed = False

flex_motor = 49
flex_steer = 49

def send_image_to_list(lst,data):
    cimg = bridge.imgmsg_to_cv2(data,"bgr8")
    advance(lst,cimg,nframes + 3)  

def right_callback(data):
    global right_list
    send_image_to_list(right_list,data)

def left_callback(data):
    global left_list
    send_image_to_list(left_list,data)

def human_agent_callback(msg):
    global human_agent
    human_agent = msg.data

def drive_mode_callback(msg):
    global drive_mode
    drive_mode = msg.data

def flex_motor__callback(msg):
    global flex_motor
    flex_motor = msg.data

def flex_steer__callback(msg):
    global flex_steer
    flex_steer = msg.data
    
def behavioral_mode_callback(msg):
    global behavioral_mode, direct, follow, furtive, play,left,right
    behavioral_mode = msg.data
    direct = 0.0
    follow = 0.0
    furtive = 0.0
    play = 0.0
    left = 0.0
    right = 0.0
    if behavioral_mode == 'left':
        left = 1.0
    if behavioral_mode == 'right':
        right = 1.0
    elif behavioral_mode == 'direct':
        direct = 1.0
    elif behavioral_mode == 'follow':
        follow = 1.0
    elif behavioral_mode == 'furtive':
        furtive = 1.0
    elif behavioral_mode == 'play':
        play = 1.0

def button_number_callback(msg):
    global left,right,button_number_previous,button_just_changed
    button_number = msg.data
    if button_number != button_number_previous:
        button_number_previous = button_number
        button_just_changed = True
        button_timer.reset()
    left = 0.0
    right = 0.0
    center = 0.0
    if button_number == 3:
        right = 1.0
    elif button_number == 1:
        left = 1.0
    else:
        center = 1.0

camera_cmd_pub = rospy.Publisher('cmd/camera', std_msgs.msg.Int32, queue_size=5)
steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=5)
motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=5)
Hz_network_pub = rospy.Publisher('Hz_network', std_msgs.msg.Float32, queue_size=5)
rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)
rospy.Subscriber('/bair_car/human_agent', std_msgs.msg.Int32, callback=human_agent_callback)
rospy.Subscriber('/bair_car/behavioral_mode', std_msgs.msg.String, callback=behavioral_mode_callback)
rospy.Subscriber('/bair_car/drive_mode', std_msgs.msg.Int32, callback=drive_mode_callback)
rospy.Subscriber('/bair_car/button_number', std_msgs.msg.Int32, callback=button_number_callback)
rospy.Subscriber('/cmd/flex_motor', std_msgs.msg.Int32, callback=flex_motor__callback)
rospy.Subscriber('/cmd/flex_steer', std_msgs.msg.Int32, callback=flex_steer__callback)

frequency_timer = Timer(1.0)
print_timer = Timer(5)

Hz = 0

low_frequency_pub_timer = Timer(0.5)

reverse_timer = Timer(1)
image_sample_timer = Timer(5)

node_timer = Timer()

Torch_network = net_utils.Torch_Network(N)

#*****
random_motor,random_steer = 49,49
rand_timer = Timer(5)

while not rospy.is_shutdown():


    if human_agent == 0 and drive_mode == 1:
        #*****
	print flex_motor,flex_steer
#*****
        if rand_timer.check():
            random_motor = 57#54
            random_steer = np.random.randint(20,80)
            random_steer = bound_value(random_steer,0,99)
            random_motor = bound_value(random_motor,0,99)
            rand_timer.reset()
            print random_steer,random_motor
	if flex_motor < 47:
		steer_val = flex_steer
		motor_val = flex_motor
	else:
		steer_val = random_steer
		motor_val = random_motor

        camera_cmd_pub.publish(std_msgs.msg.Int32(49))
        steer_cmd_pub.publish(std_msgs.msg.Int32(steer_val))
        motor_cmd_pub.publish(std_msgs.msg.Int32(motor_val))


    else:
        print 'waiting...'
        time.sleep(0.1)

CS_('goodbye!',__file__)
#default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)



#EOF

    
