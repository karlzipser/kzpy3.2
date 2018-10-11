#!/usr/bin/env python

from kzpy3.utils3 import *

#from Default_values.network.default_values import N

#import Default_values.network.default_values.N as N
#from network_menu_thread import *
#exec(identify_file_str)



import kzpy3.Cars.n30Sept2018_car_with_nets.nodes.Default_values.network.default_values as default_values
N = default_values.N
N['ABORT'] = False
import kzpy3.Menu_app.menu
menu_path = opjh("kzpy3/Cars/n30Sept2018_car_with_nets/nodes/Default_values/network")
if not os.path.exists(menu_path):
    os.makedirs(menu_path)
#threading.Thread(target=kzpy3.Menu_app.menu.load_menu_data,args=[menu_path,N]).start()



import rospy

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

frequency_timer = Timer(1.0)
print_timer = Timer(5)

Hz = 0

low_frequency_pub_timer = Timer(0.5)

reverse_timer = Timer(1)
image_sample_timer = Timer(5)

node_timer = Timer()

Torch_network = net_utils.Torch_Network(N)

while not rospy.is_shutdown():

    if node_timer.time() > 10:
        if len(left_list) == 0:
            for i in range(5):
                pass
                #CS_("empty image list after 30s, ABORTING, rebooting!!!!!",emphasis=True)
            #default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)
    if False:
        if len(left_list) > 0:
            if image_sample_timer.check():
                img = left_list[1]
                print(img[0:15,0,0])
                print np.sum(img[0:100,0,0])
                image_sample_timer.reset()

    time.sleep(0.001)
    Hz = frequency_timer.freq(name='Hz_network',do_print=False)
    if is_number(Hz):
        if low_frequency_pub_timer.check():
            Hz_network_pub.publish(std_msgs.msg.Float32(Hz))
            low_frequency_pub_timer.reset()

    s1 = N['network_motor_smoothing_parameter']
    s2 = N['network_servo_smoothing_parameter']
    s3 = N['network_camera_smoothing_parameter']

    if human_agent == 0 and drive_mode == 1:
        if len(left_list) > nframes + 2:
            camera_data = Torch_network['format_camera_data'](left_list,right_list)
            metadata = Torch_network['format_metadata']((direct,follow,furtive,play,left,right)) #((right,left,play,furtive,follow,direct))
            torch_motor, torch_steer = Torch_network['run_model'](camera_data, metadata, N)
            """
            Torch_network['output'] should contain full output array of network
            """


            if 'Do smoothing of percents...':
                current_camera = (1.0-s3)*torch_steer + s3*current_camera
                current_steer = (1.0-s2)*torch_steer + s2*current_steer
                current_motor = (1.0-s1)*torch_motor + s1*current_motor

            if button_just_changed:
                #print "button_just_changed"
                button_just_changed = False
                if left:
                    pass
                    #print('left')
                    #current_camera = 99
                elif right:
                    pass
                    #current_camera = 0
                    #print('right')
                else:
                    current_camera = 49
                    #print('center')

            adjusted_motor = int(N['network_motor_gain']*(current_motor-49) + N['network_motor_offset'] + 49)
            adjusted_steer = int(N['network_steer_gain']*(current_steer-49) + 49)
            adjusted_camera = int(N['network_camera_gain']*(current_camera-49) + 49)



            #print left,right




            adjusted_motor = bound_value(adjusted_motor,0,99)
            adjusted_steer = bound_value(adjusted_steer,0,99)
            adjusted_camera = bound_value(adjusted_camera,0,99)
            
            print adjusted_camera,adjusted_steer,adjusted_motor

            camera_cmd_pub.publish(std_msgs.msg.Int32(adjusted_camera))
            steer_cmd_pub.publish(std_msgs.msg.Int32(adjusted_steer))
            motor_cmd_pub.publish(std_msgs.msg.Int32(adjusted_motor))

        if N['visualize_activations']:
            Net_activity = Activity_Module.Net_Activity('batch_num',0, 'activiations',Torch_network['solver'].A)
            Net_activity['view']('moment_index',0,'delay',1, 'scales',{'camera_input':1,'pre_metadata_features':0,'pre_metadata_features_metadata':1,'post_metadata_features':1})
            cv2.waitKey(1)#spause()

    else:
        time.sleep(0.1)

CS_('goodbye!',__file__)
#default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)



#EOF

    