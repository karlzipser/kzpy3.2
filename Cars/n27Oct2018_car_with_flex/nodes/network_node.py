#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)
sbpd2s("network_node.py")

import kzpy3.Cars.n11Oct2018_car_with_nets.nodes.Default_values.arduino.default_values as default_values
N = default_values.P

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
button_number = 0;
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
    global left,right,button_number,button_number_previous,button_just_changed
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

flex_names = []
for fb in ['F']:
    for lr in ['L','C','R']:
        for i in [0,1,2,3]:
            flex_names.append(d2n(fb,lr,i))

F = {}
for f in flex_names:
    s = """
F['FLEX'] = []
def FLEX__callback(msg):
    advance(F['FLEX'],msg.data,18)
rospy.Subscriber('/bair_car/FLEX', std_msgs.msg.Int32, callback=FLEX__callback)
    """
    exec_str = s.replace('FLEX',f)
    exec(exec_str)

camera_cmd_pub = rospy.Publisher('cmd/camera', std_msgs.msg.Int32, queue_size=5)
steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=5)
motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=5)
flex_steer_cmd_pub = rospy.Publisher('cmd/flex_steer', std_msgs.msg.Int32, queue_size=5)
flex_motor_cmd_pub = rospy.Publisher('cmd/flex_motor', std_msgs.msg.Int32, queue_size=5)
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

ZED_torch_network = None

loaded_net = False

import kzpy3.Menu_app.menu2 as menu2

import kzpy3.Data_app.collect_flex_data2 as fx

parameter_file_load_timer = Timer(0.5)

while not rospy.is_shutdown():

    if button_number == 4:

        time.sleep(1)

        if parameter_file_load_timer.check():

            Topics = menu2.load_Topics(
                opjk("Cars/n11Oct2018_car_with_nets/nodes/Default_values/arduino"),
                first_load=False,
                customer='Network Node')
            
            if type(Topics) == dict:
                for t in Topics['To Expose']['Network Node']+Topics['To Expose']['Trained Nets']:
                    if '!' in t:
                        pass
                    else:
                        N[t] = Topics[t]

            parameter_file_load_timer.reset()


        if N['LOAD NETWORK'] == False:
            loaded_net = False


        
        N['weight_file_path'] = False
        cs("loaded_net=",loaded_net)
        if loaded_net == False:
            if N['LOAD NETWORK'] == True:
                loaded_net = True
                
                ns = N['weight_files'].keys()

                for n in ns:

                    if N[n] != False:

                        if type(N[n]) == list:

                            if N[n][0] != False:

                                if N[n][0] == True:
                                    N['weight_file_path'] = N['weight_files'][n][N[n][1]]
                                    srpd2s("N['weight_file_path'] = N['weight_files'][n][a[1]]")
                                    break

                if N['weight_file_path'] != False:
                    cs( "if N['weight_file_path'] != False:" )
                    ZED_torch_network = net_utils.ZED_Torch_Network(N)
                    cs( "ZED_torch_network = net_utils.ZED_Torch_Network(N)" )


    if ZED_torch_network == None:
        continue

    Flex_torch_network = net_utils.Flex_Torch_Network(N)

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
            camera_data = ZED_torch_network['format_camera_data'](left_list,right_list)
            metadata = ZED_torch_network['format_metadata']((direct,follow,furtive,play,left,right)) #((right,left,play,furtive,follow,direct))
            torch_motor, torch_steer = ZED_torch_network['run_model'](camera_data, metadata, N)

            #Fs = take flex data and put into appropriate flex segment format 
            flex_data = Flex_torch_network['format_flex_data'](fx.make_flex_image(Fs))
            flex_torch_motor, flex_torch_steer = Flex_torch_network['run_model'](camera_data, N)


            if 'Do smoothing of percents...':
                current_camera = (1.0-s3)*torch_steer + s3*current_camera
                current_steer = (1.0-s2)*torch_steer + s2*current_steer
                current_motor = (1.0-s1)*torch_motor + s1*current_motor



            adjusted_motor = int(N['network_motor_gain']*(current_motor-49) + N['network_motor_offset'] + 49)
            adjusted_steer = int(N['network_steer_gain']*(current_steer-49) + 49)
            adjusted_camera = int(N['network_camera_gain']*(current_camera-49) + 49)

            adjusted_motor = bound_value(adjusted_motor,0,99)
            adjusted_steer = bound_value(adjusted_steer,0,99)
            adjusted_camera = bound_value(adjusted_camera,0,99)
            
            #print adjusted_camera,adjusted_steer,adjusted_motor

            camera_cmd_pub.publish(std_msgs.msg.Int32(adjusted_camera))
            steer_cmd_pub.publish(std_msgs.msg.Int32(adjusted_steer))
            motor_cmd_pub.publish(std_msgs.msg.Int32(adjusted_motor))
            flex_steer_cmd_pub.publish(std_msgs.msg.Int32(flex_torch_steer))
            flex_cmd_pub.publish(std_msgs.msg.Int32(flex_torch_motor))
    else:
        time.sleep(0.1)

CS_('goodbye!',__file__)
CS_("doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))")
time.sleep(0.01)
unix(opjh('kzpy3/scripts/kill_ros.sh'))
#default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)



#EOF

    