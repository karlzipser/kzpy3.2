#!/usr/bin/env python
from kzpy3.utils2 import *
import default_values
exec(identify_file_str)

N = {}
for k in default_values.Network.keys():
    N[k] = default_values.Network[k]

import kzpy3.Menu_app.menu
menu_path = opjh('.menu','network_node')
unix('mkdir -p '+menu_path)
unix(d2s('rm',opj(menu_path,'ready')))
threading.Thread(target=kzpy3.Menu_app.menu.load_menu_data,args=[menu_path,N]).start()


if not N['USE_NETWORK']:
    spd2s('network_node.py::not using network')
    time.sleep(3600*24)
    assert(False)
import net_utils

#################################################################################
#
if False:
    if 'This is the paramiko setup section':
        paramiko_steer,paramiko_motor = 49,49
        SEND_STEER_MOTOR_WITH_PARAMIKO = False
        try:
            if os.environ['PARAMIKO_TARGET_IP']:
                os.environ['PARAMIKO_TARGET_IP']
                import paramiko

                sshclient = paramiko.SSHClient()
                sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                sshclient.connect(os.environ['PARAMIKO_TARGET_IP'],username='nvidia')
                paramiko_freq_timer = Timer(5)
                paramiko_path = opjD('paramiko')
                spd2s('Using paramiko to send steer/motor signals to',os.environ['PARAMIKO_TARGET_IP'])
                SEND_STEER_MOTOR_WITH_PARAMIKO = True
        except Exception as e:
            pass
            print("********** PARAMIKO_TARGET_IP Exception ***********************")
            print(e.message, e.args)
        RECEIVE_STEER_MOTOR_FROM_PARAMIKO = False
        try:
            if os.environ['RECEIVE_STEER_MOTOR_FROM_PARAMIKO'] == 'True':
                if SEND_STEER_MOTOR_WITH_PARAMIKO == False:
                    RECEIVE_STEER_MOTOR_FROM_PARAMIKO = True
                    spd2s('Using paramiko to receive steer/motor signals because',"os.environ['RECEIVE_STEER_MOTOR_FROM_PARAMIKO'] =",os.environ['RECEIVE_STEER_MOTOR_FROM_PARAMIKO'])
        except Exception as e:
            pass
            print("********** RECEIVE_STEER_MOTOR_FROM_PARAMIKO Exception ***********************")
            print(e.message, e.args)
#
#################################################################################


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
    global left,right
    button_number = msg.data
    left = 0.0
    right = 0.0
    if button_number == 3:
        right = 1.0
    elif button_number == 1:
        left = 1.0

"""
def network_weights_name_callback(msg):
    s = msg.data
    if s != N['weight_file_path']:
        N['weight_file_path'] = s
        N['RELOAD_NET'] = True
    else:
        N['RELOAD_NET'] = False
"""

"""
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
"""

camera_cmd_pub = rospy.Publisher('cmd/camera', std_msgs.msg.Int32, queue_size=100)
steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=100)
motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=100)
Hz_network_pub = rospy.Publisher('Hz_network', std_msgs.msg.Float32, queue_size=5)
rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)
rospy.Subscriber('/bair_car/human_agent', std_msgs.msg.Int32, callback=human_agent_callback)
rospy.Subscriber('/bair_car/behavioral_mode', std_msgs.msg.String, callback=behavioral_mode_callback)
#rospy.Subscriber('/bair_car/network_weights_name', std_msgs.msg.String, callback=network_weights_name_callback)
rospy.Subscriber('/bair_car/drive_mode', std_msgs.msg.Int32, callback=drive_mode_callback)
rospy.Subscriber('/bair_car/button_number', std_msgs.msg.Int32, callback=button_number_callback)
"""
rospy.Subscriber('/network_output_sample', std_msgs.msg.Int32, callback=callback_network_output_sample)
rospy.Subscriber('/network_motor_offset', std_msgs.msg.Int32, callback=callback_network_motor_offset)
rospy.Subscriber('/network_steer_gain', std_msgs.msg.Float32, callback=callback_network_steer_gain)
rospy.Subscriber('/network_motor_gain', std_msgs.msg.Float32, callback=callback_network_motor_gain)
rospy.Subscriber('/network_smoothing_parameter', std_msgs.msg.Float32, callback=callback_network_smoothing_parameter)
"""


N['RELOAD_NET'] = True
frequency_timer = Timer(1.0)
print_timer = Timer(5)

Hz = 0


low_frequency_pub_timer = Timer(0.5)

#Torch_network = net_utils.Torch_Network(N)
if N['visualize_activations']:
    import cv2
    from kzpy3.vis2 import *
    from Train_SqueezeNet_31May3018_copy import Activity_Module 

DRIVE_FORWARD = True
reverse_timer = Timer(1)

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

    s1 = N['network_motor_smoothing_parameter']
    s2 = N['network_servo_smoothing_parameter']
    s3 = N['network_camera_smoothing_parameter']
    #print_timer.message(d2s('network_node::drive_mode =',drive_mode))#######

    if human_agent == 0 and drive_mode == 1:
        if len(left_list) > nframes + 2:
            camera_data = Torch_network['format_camera_data'](left_list,right_list)
            metadata = Torch_network['format_metadata']((direct,follow,furtive,play,left,right)) #((right,left,play,furtive,follow,direct))
            torch_motor, torch_steer = Torch_network['run_model'](camera_data, metadata, N)
            """
            Torch_network['output'] should contain full output array of network
            """

            if 'Do smoothing of percents...':
                current_camera = (1.0-s3)*torch_steer + s3*current_steer
                current_steer = (1.0-s2)*torch_steer + s2*current_steer
                current_motor = (1.0-s1)*torch_motor + s1*current_motor

            adjusted_motor = int(N['network_motor_gain']*(current_motor-49) + N['network_motor_offset'] + 49)
            adjusted_steer = int(N['network_steer_gain']*(current_steer-49) + 49)
            adjusted_camera = int(N['network_steer_gain']*(current_camera-49) + 49)

            adjusted_motor = bound_value(adjusted_motor,0,99)
            adjusted_steer = bound_value(adjusted_steer,0,99)
            adjusted_camera = bound_value(adjusted_camera,0,99)

            #################################################################################
            #
            if False:
                if 'This is the paramiko runtime section':

                    if RECEIVE_STEER_MOTOR_FROM_PARAMIKO:
                        try:
                            paramiko_values_good = False
                            the_file,seconds_old = most_recent_file_in_folder(opjD('paramiko'),return_age_in_seconds=True)
                            latest_paramiko_message = fname(the_file)
                            _files = glob.glob(opjD('paramiko','*'))
                            for f in _files:
                                os.remove(f)
                            if type(latest_paramiko_message) == str:
                                if seconds_old < 0.1:
                                    print latest_paramiko_message,dp(seconds_old,3)
                                    components = latest_paramiko_message.split('.')
                                    paramiko_steer = num_from_str(components[0])
                                    paramiko_motor = num_from_str(components[1])
                                    paramiko_values_good = False
                                    if components[2] == 'cmd':
                                        if type(paramiko_steer) == int:
                                            if paramiko_steer >= 0:
                                                if paramiko_steer < 100:
                                                    if type(paramiko_motor) == int:
                                                        if paramiko_motor >= 0:
                                                            if paramiko_motor < 100:
                                                                paramiko_values_good = True
                                """
                                else:
                                    paramiko_steer,paramiko_motor = 49,49
                                    paramiko_values_good = True # good in the sense that they can be used 
                                if paramiko_values_good:
                                """
                                #pd2s('(',paramiko_steer,',',paramiko_motor,')\t(',adjusted_steer,',',adjusted_motor,')')
                        except Exception as e:
                            pass
                            #print("********** if RECEIVE_STEER_MOTOR_FROM_PARAMIKO: Exception ***********************")
                            #print(e.message, e.args)



                    elif SEND_STEER_MOTOR_WITH_PARAMIKO:
                        try:
                            filename = d2p(int(adjusted_steer),int(adjusted_motor),'cmd')
                            paramiko_freq_timer.freq(filename)
                            sshclient.exec_command(d2n('touch ',opj(paramiko_path,filename)))
                        except Exception as e:
                            pass
                            print("********** elif SEND_STEER_MOTOR_WITH_PARAMIKO: Exception ***********************")
                            print(e.message, e.args)


                
                if RECEIVE_STEER_MOTOR_FROM_PARAMIKO:
                    if DRIVE_FORWARD == True:
                        reverse_timer.reset()
                        if adjusted_motor < N['motor_reverse_threshold']:
                            #pd2s(paramiko_motor, '>', N['motor_reverse_threshold'],'?')
                            if True:#paramiko_motor > N['motor_reverse_threshold']:
                                #print 'B'
                                DRIVE_FORWARD = False
                                #print 'reset'
                                #reverse_timer.reset()
                    if DRIVE_FORWARD == False:
                        if reverse_timer.check():
                            DRIVE_FORWARD = True
                            #
                        if False and paramiko_motor < N['motor_reverse_threshold'] and adjusted_motor > N['motor_reverse_threshold']:
                            DRIVE_FORWARD = True
                            #
                    if DRIVE_FORWARD == False:
                        adjusted_motor = bound_value(99-paramiko_motor,0,99)
                        adjusted_steer = bound_value(99-adjusted_steer,0,99)                    
                        #adjusted_steer = bound_value(99-paramiko_steer,0,99)
                        #adjusted_motor = bound_value(paramiko_motor,0,99)
                        #adjusted_steer = bound_value(paramiko_steer,0,99)
                #
                #################################################################################
                if False:
                    if DRIVE_FORWARD:
                        _m = '['
                        _n = ']'
                    else:
                        _m = '<'
                        _n = '>'
                    pd2s(_m,DRIVE_FORWARD,adjusted_steer,',',adjusted_motor,_n,dp(reverse_timer.time(),1),SEND_STEER_MOTOR_WITH_PARAMIKO,RECEIVE_STEER_MOTOR_FROM_PARAMIKO)


            #################################################################################
            #
            camera_cmd_pub.publish(std_msgs.msg.Int32(adjusted_camera))
            steer_cmd_pub.publish(std_msgs.msg.Int32(adjusted_steer))
            motor_cmd_pub.publish(std_msgs.msg.Int32(adjusted_motor))
            #
            #################################################################################







        if N['visualize_activations']:#low_frequency_pub_timer2.check():
            #mi(np.random.random((100,100)));spause()
            Net_activity = Activity_Module.Net_Activity('batch_num',0, 'activiations',Torch_network['solver'].A)
            Net_activity['view']('moment_index',0,'delay',1, 'scales',{'camera_input':1,'pre_metadata_features':0,'pre_metadata_features_metadata':1,'post_metadata_features':1})
            #pd2s("N['weight_file_path'] =",N['weight_file_path'])
            cv2.waitKey(1)#spause()
            #spd2s(adjusted_steer,adjusted_motor,drive_mode, human_agent, behavioral_mode)
            #low_frequency_pub_timer2.reset()
    else:
        #print 'network paused'
        time.sleep(0.1)

print 'goodbye!'
print "unix(opjh('kzpy3/kill_ros.sh'))"
unix(opjh('kzpy3/kill_ros.sh'))


#EOF

    