#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)
sbpd2s("network_node.py")

"""
python kzpy3/Cars/n9Nov2018/nodes/network_node.py show_net_input 0
"""




torch_steer,torch_motor = 49,49





####################################################
####################################################
####################################################
##


from kzpy3.vis3 import *
import rospy
import roslib
import std_msgs.msg
import geometry_msgs.msg
import cv2
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image##
bridge = CvBridge()
exec(identify_file_str)



import kzpy3.Data_app.lidar.python_pointclouds6k as ppc

for a in Arguments:
    ppc.A[a] = Arguments[a]

left_list = []
right_list = []
lidar_list = []

nframes = 2
left_calls = 0
left_calls_prev = 0
left_timer = Timer(5)

def send_image_to_list(lst,data):
    cimg = bridge.imgmsg_to_cv2(data,"bgr8")
    advance(lst,cimg,nframes + 3)  

def right_callback(data):
    global right_list
    send_image_to_list(right_list,data)
#lts = []
def left_callback(data):
    global left_list, left_calls
    send_image_to_list(left_list,data)
    left_calls += 1
    left_timer.freq('left_timer')

#rospy.init_node('network_node',anonymous=True,disable_signals=True)
rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)



##############################################
#
# visualization only
rgb_spacer = zeros((94,2),np.uint8)+128
t_spacer = zeros((4,508),np.uint8)+128
lr_spacer = zeros((200,8),np.uint8)+128
def rgbcat(L,s,t):
    return np.concatenate(( L[s][t][:,:,0],rgb_spacer, L[s][t][:,:,1],rgb_spacer, L[s][t][:,:,2] ),axis=1)
def tcat(t0,tn1):
    return np.concatenate( (t_spacer,t0,t_spacer,tn1,t_spacer), axis=0)
def lrcat(l,r):
    return np.concatenate( (lr_spacer,l,lr_spacer,r,lr_spacer), axis=1)
#
##############################################

##############################################
#
threading.Thread(target=ppc.pointcloud_thread,args=[]).start()
#
##############################################

Durations = {}
durations = ['fuse images',]
for d in durations:
    Durations[d] = {}
    Durations[d]['timer'] = Timer()
    Durations[d]['list'] = []
show_durations = Timer(5)

net_input_width = 168
net_input_height = 94
resize = ppc.resize_versions[0]
image_type = ppc.image_type_versions[0]
mn,mx = -0.5,0.7

waiting = Timer(1)
frequency_timer = Timer(5)


##
####################################################
####################################################
####################################################
            






































import kzpy3.Cars.n9Nov2018.nodes.Default_values.arduino.default_values as default_values
N = default_values.P

import rospy
import net_utils
import roslib
import std_msgs.msg


rospy.init_node('network_node',anonymous=True,disable_signals=True)

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

frequency_timer = Timer(5.0)
print_timer = Timer(5)

reverse_timer = Timer(1)
image_sample_timer = Timer(5)

node_timer = Timer()

Torch_network = None

loaded_net = False

import kzpy3.Menu_app.menu2 as menu2

parameter_file_load_timer = Timer(0.5)



# TEMPORARY
human_agent = 0   ##########################
drive_mode = 1    ##########################
button_number = 4 ##########################

while not rospy.is_shutdown():
    #print button_number
    if Torch_network != None: ##########################
        button_number = 2 ##########################

    if button_number == 4: 

        time.sleep(1)

        if parameter_file_load_timer.check():

            Topics = menu2.load_Topics(
                opjk("Cars/n9Nov2018_car_with_nets/nodes/Default_values/arduino"),
                first_load=False,
                customer='Network Node')
            
            if type(Topics) == dict:
                for t in Topics['To Expose']['Network Node']+Topics['To Expose']['Trained Nets']:
                    if '!' in t:
                        pass
                    else:
                        N[t] = Topics[t]

            parameter_file_load_timer.reset()


        #if N['LOAD NETWORK'] == False:
        #    loaded_net = False

        Torch_network = net_utils.Torch_Network(N)   ##########################
        
        """
        N['weight_file_path'] = False
        cs("loaded_net=",loaded_net)
        if loaded_net == False:
            if N['LOAD NETWORK'] == True:
                loaded_net = True
                ns = N['weight_files'].keys()
                for n in ns:
                    cs(n,N[n])
                    if N[n] != False:
                        if type(N[n]) == list:
                            if N[n][0] != False:
                                if N[n][0] == True:
                                    N['weight_file_path'] = N['weight_files'][n][N[n][1]]
                                    srpd2s("N['weight_file_path'] = N['weight_files'][n][a[1]]")
                                    break

                if N['weight_file_path'] != False:
                    cs( "if N['weight_file_path'] != False:" )
                    Torch_network = net_utils.Torch_Network(N)
                    cs( "Torch_network = net_utils.Torch_Network(N)" )
        """

    #if Torch_network == None:
    #    continue
    try:
        time.sleep(0.001)

        s1 = N['network_motor_smoothing_parameter']
        s2 = N['network_servo_smoothing_parameter']
        s3 = N['network_camera_smoothing_parameter']
        #cr('A')
        human_agent = 0   ##########################
        drive_mode = 1    ##########################
        #print len(left_list)
        if human_agent == 0 and drive_mode == 1:
            if len(left_list) > nframes + 2:
                cr('B')
                #cb(time.time())
                frequency_timer.freq(name='network',do_print=True)
                ####################################################
                ####################################################
                ####################################################
                ##
                if (left_calls > left_calls_prev):

                    dname = 'fuse images'
                    print Durations[dname]['timer'].reset()

                    cr('C')
                    print Durations[dname]['timer'].time()
                    k = image_type+'_resized_'+resize
                    if k in ppc.Images:
                        img = ppc.Images[k]
                        if image_type == 't':
                            img = np.log10(img+0.001)
                            img[img>mx] = mx
                            img[img<mn] = mn
                            if 'temporary (?)':
                                img[0,0] = mx; img[0,1] = mn
                            img = (z2o(img)*255).astype(np.uint8)
                        #advance(lidar_list,img,7)
                        lidar_list.append(img)
                        if len(lidar_list)>10:
                            lidar_list = lidar_list[-10:]
                    print Durations[dname]['timer'].time()
                    Lists = {}
                    Lists['left'] = left_list[-2:]
                    Lists['right'] = right_list[-2:]##
                    rLists = {}
                    rLists['left'] = []
                    rLists['right'] = []
                    for side in ['left','right']:
                        for i in [-1,-2]:
                            rLists[side].append( cv2.resize(Lists[side][i],(net_input_width,net_input_height)) )
                    print Durations[dname]['timer'].time()
                    if len(lidar_list) > 4:
                        #print len(lidar_list)
                        rLists['left'][-2][:,:,1] = lidar_list[-1]
                        rLists['left'][-2][:,:,2] = lidar_list[-2]

                        rLists['right'][-2][:,:,1] = lidar_list[-3]
                        rLists['right'][-2][:,:,2] = lidar_list[-4]

                        #so(rLists,opjD('rLists'))
                        #raw_enter()

                        #print shape(rLists['left'][0]), shape(rLists['right'][0])
                        #mi(rLists['left'][0],0)
                        #mi(rLists['left'][1],1)
                        #mi(rLists['right'][0],10)
                        #mi(rLists['right'][1],11)
                        #spause()

                    print Durations[dname]['timer'].time()
                    Durations[dname]['list'].append(1000.0*Durations[dname]['timer'].time())
                    cr('D')
                    if 'show_net_input' in Arguments:

                        if ppc.A['show_net_input']:

                            l0 = rgbcat(rLists,'left',-1)
                            ln1 = rgbcat(rLists,'left',-2)
                            r0 = rgbcat(rLists,'right',-1)
                            rn1 = rgbcat(rLists,'right',-2)
                            l = tcat(l0,ln1)
                            r = tcat(r0,rn1)
                            lr = lrcat(l,r)

                            mci((z2o(lr)*255).astype(np.uint8),scale=1.0,color_mode=cv2.COLOR_GRAY2BGR,title='ZED')

                    cr('E')
                    if show_durations.check():
                        for d in durations:
                            cg(d,':',dp(np.median(Durations[d]['list']),1),'ms')
                        show_durations.reset()

                        

                else:
                    pass
                cr('F')
        

                ##
                ####################################################
                ####################################################
                ####################################################
                










                ####################################################
                #(2, 94, 168, 3) (94, 168, 3)
                #(5, 376, 672, 3) (376, 672, 3)
                camera_data = Torch_network['format_camera_data__no_scale'](rLists['left'][:],rLists['right'][:])
                #camera_data = Torch_network['format_camera_data'](left_list,right_list)
                #
                ####################################################
                metadata = Torch_network['format_metadata']((direct,follow,furtive,play,left,right)) #((right,left,play,furtive,follow,direct))
                torch_motor, torch_steer = Torch_network['run_model'](camera_data, metadata, N)

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
                
                #print adjusted_steer,adjusted_motor

                camera_cmd_pub.publish(std_msgs.msg.Int32(adjusted_camera))
                steer_cmd_pub.publish(std_msgs.msg.Int32(adjusted_steer))
                motor_cmd_pub.publish(std_msgs.msg.Int32(adjusted_motor))
                
            ####################################################
            ####################################################
            ####################################################
            ##
            left_calls_prev = left_calls
            ##    
            ####################################################
            ####################################################
            ####################################################

        else:
            pass

        if show_durations.check():
            for d in durations:
                cg(d,':',np.median(Durations[d]['list']),'ms')
                #cg(d,':',dp(np.median(Durations[d]['list']),1),'ms')
                show_durations.reset()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)





CS_('goodbye!',__file__)
CS_("doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))")
time.sleep(0.01)
unix(opjh('kzpy3/scripts/kill_ros.sh'))
#default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)



#EOF

    