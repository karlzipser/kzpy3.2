#!/usr/bin/env python
from kzpy3.vis3 import *
exec(identify_file_str)
sbpd2s("network_node.py")

import Activity_Module
#import kzpy3.Train_app.Train_SqueezeNet_15Sept2018_1Nov_14Nov.Activity_Module as Activity_Module
"""

this is the current working version for lidar and camera as of 12 Nov. 2018 (evening)

"""

import default_values
N = default_values.P

import rospy
import torch
import net_utils
import roslib
import std_msgs.msg
import geometry_msgs.msg
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
bridge = CvBridge()
import cv2

dts = []

show_timer = Timer(1)

if N['use LIDAR']:
    #cy("if N['use LIDAR']:")
    import kzpy3.Data_app.lidar.python_pointclouds6k as ppc
    resize = ppc.resize_versions[0]
    image_type = ppc.image_type_versions[0]
    lidar_list = []
rospy.init_node('network_node',anonymous=True,disable_signals=True)

left_list = []
right_list = []
nframes = 2 #figure out how to get this from network

even = True

nframes = 2
left_calls = 0
left_calls_prev = 0
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
    global left_list, left_calls
    send_image_to_list(left_list,data)
    left_calls += 1

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

flex_motor = 49
flex_steer = 49

def flex_motor__callback(msg):
    global flex_motor
    flex_motor = msg.data

def flex_steer__callback(msg):
    global flex_steer
    flex_steer = msg.data

camera_cmd_pub = rospy.Publisher('cmd/camera', std_msgs.msg.Int32, queue_size=5)
steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=5)
motor_cmd_pub = rospy.Publisher('cmd/motor', std_msgs.msg.Int32, queue_size=5)
Hz_network_pub = rospy.Publisher('Hz_network', std_msgs.msg.Float32, queue_size=5)

rospy.Subscriber('/bair_car/human_agent', std_msgs.msg.Int32, callback=human_agent_callback)
rospy.Subscriber('/bair_car/behavioral_mode', std_msgs.msg.String, callback=behavioral_mode_callback)
rospy.Subscriber('/bair_car/drive_mode', std_msgs.msg.Int32, callback=drive_mode_callback)
rospy.Subscriber('/bair_car/button_number', std_msgs.msg.Int32, callback=button_number_callback)

if N['use flex']:
    rospy.Subscriber('/bair_car/cmd/flex_motor', std_msgs.msg.Int32, callback=flex_motor__callback)
    rospy.Subscriber('/bair_car/cmd/flex_steer', std_msgs.msg.Int32, callback=flex_steer__callback)

if not N['lidar_only']:
    rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
    rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)














#############################################################################################
#############################################################################################
##        Making metadata tensors in advance so they need not be constructed during runtime.
##        For SqueezeNet40 models
TP = {}
TP['behavioral_modes_no_heading_pause'] = ['direct','follow','furtive','play','left','right']
# note, 'center' is not included in TP['behavioral_modes_no_heading_pause'] because 'center' is converted to 'direct' below.
TP['behavioral_modes'] = TP['behavioral_modes_no_heading_pause']+['heading_pause']

zero_matrix = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()
one_matrix = torch.FloatTensor(1, 1, 23, 41).fill_(1).cuda()

Metadata_tensors = {}

for the_behaviorial_mode in TP['behavioral_modes']:

    Metadata_tensors[the_behaviorial_mode] = torch.FloatTensor().cuda()

    mode_ctr = 0

    metadata = torch.FloatTensor().cuda()

    for cur_label in TP['behavioral_modes']:

        if cur_label == the_behaviorial_mode:
            
            #if Data_moment['labels'][cur_label]:
                
            metadata = torch.cat((one_matrix, metadata), 1); mode_ctr += 1
        else:
            metadata = torch.cat((zero_matrix, metadata), 1); mode_ctr += 1
        #else:
        #   metadata = torch.cat((zero_matrix, metadata), 1); mode_ctr += 1

    num_metadata_channels = 128
    num_multival_metas = 5
    for i in range(num_metadata_channels - num_multival_metas - mode_ctr):
        # Concatenate zero matrices to fit the dataset
        metadata = torch.cat((zero_matrix, metadata), 1)

    meta_gradient1 = zero_matrix.clone()
    for x in range(23):
        meta_gradient1[:,:,x,:] = x/23.0
    metadata = torch.cat((meta_gradient1, metadata), 1)

    meta_gradient2 = zero_matrix.clone()
    for x in range(23):
        meta_gradient2[:,:,x,:] = (1.0-x/23.0)
    metadata = torch.cat((meta_gradient2, metadata), 1)

    meta_gradient3 = zero_matrix.clone()
    for x in range(41):
        meta_gradient3[:,:,:,x] = x/41.0
    metadata = torch.cat((meta_gradient3, metadata), 1)

    meta_gradient4 = zero_matrix.clone()
    for x in range(41):
        meta_gradient4[:,:,:,x] = (1.0-x/41.0)
    metadata = torch.cat((meta_gradient4, metadata), 1)
    
    for topic in ['encoder']:
        #
        typical_encoder_value = 2.0
        d = typical_encoder_value / 100.0 / 5.0
        #d = Data_moment[topic+'_past']/100.0
        #if topic == 'encoder':
            #med = np.median(d)
            #for i in range(len(d)):
            #   if d[i] < med/3.0:
            #       d[i] = med # this to attempt to get rid of drop out from magnet not being read
            #d = d/5.0
        #d = d.reshape(-1,3).mean(axis=1)
        #for x in range(0,23):
        #   meta_gradient5[:,:,x,:] = d[x]
        meta_gradient5 = zero_matrix.clone() + d
        metadata = torch.cat((meta_gradient5, metadata), 1)
        
    Metadata_tensors[the_behaviorial_mode] = torch.cat((metadata, Metadata_tensors[the_behaviorial_mode]), 0)
##
#############################################################################################
#############################################################################################






















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
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if N['use LIDAR']:
    threading.Thread(target=ppc.pointcloud_thread,args=[]).start()
    #cy("if N['use LIDAR']: 290")
#
##############################################

Durations = {}
durations = ['fuse images','torch camera format','run mode']
for d in durations:
    Durations[d] = {}
    Durations[d]['timer'] = Timer()
    Durations[d]['list'] = []
show_durations = Timer(5)

net_input_width = 168
net_input_height = 94

mn,mx = -0.25,1.5

waiting = Timer(1)
frequency_timer = Timer(5)


##
####################################################
####################################################
####################################################
            












#first_time = True






rLists = {}
rLists['left'] = []
rLists['right'] = []


print_timer = Timer(5)

Hz = 0

low_frequency_pub_timer = Timer(0.5)

reverse_timer = Timer(1)
image_sample_timer = Timer(5)

node_timer = Timer()

Torch_network = None

loaded_net = False

import kzpy3.Menu_app.menu2 as menu2

parameter_file_load_timer = Timer(1)

torch_motor, torch_steer, torch_camera = 49,49,49

while not rospy.is_shutdown():

    #cr('Z')

    #####################################################################
    #####################################################################
    ###    
    if button_number == 4:

        time.sleep(1)

        if parameter_file_load_timer.check():

            Topics = menu2.load_Topics(
                opjk("Cars/n11Oct2018_car_with_nets/nodes"),
                first_load=False,
                customer='Network')
            
            if type(Topics) == dict:
                for t in Topics['To Expose']['Network']+Topics['To Expose']['Weights']+Topics['To Expose']['Flex']:
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
                cs(ns)
                for n in ns:
                    cs('A')
                    cs(n,N[n])
                    if N[n] != False:
                        cs('B')
                        if type(N[n]) == list:
                            cs('C')
                            if N[n][0] != False:
                                cs('D')
                                cs('here',n,N[n])
                                if N[n][0] == True:
                                    cs('E')
                                    N['weight_file_path'] = N['weight_files'][n][N[n][1]]
                                    sbpd2s("N['weight_file_path'] = N['weight_files'][n][a[1]]")
                                    break

                if N['weight_file_path'] != False:
                    cs( "if N['weight_file_path'] != False:" )
                    Torch_network = net_utils.Torch_Network(N)
                    cs( "Torch_network = net_utils.Torch_Network(N)" )




    ###
    #####################################################################
    #####################################################################
    

    if Torch_network == None:
        #cy("if Torch_network == None:")
        time.sleep(0.1)
        continue
    #else print Torch_network

    time.sleep(0.001)





    if human_agent == 0 and drive_mode == 1:

        #frequency_timer.freq(name='Hz_network',do_print=False)


        #cr('A')

        #cy("if human_agent == 0 and drive_mode == 1:")
        try:
        #if len(left_list) > nframes + 1 or len(lidar_list)>3:
            #cr('B')
            #cb(time.time())
            
            ####################################################
            ####################################################
            ####################################################
            ##
            if True:#(left_calls > left_calls_prev):

                #dname = 'fuse images'
                #Durations[dname]['timer'].reset()

                #cr('C')
                #print Durations[dname]['timer'].time()

                if N['use LIDAR']:
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
                        if len(lidar_list)>5:
                            lidar_list = lidar_list[-5:]
                        #cy(shape(lidar_list))
                
                #print Durations[dname]['timer'].time()
                #cr('C1')
                if not N['lidar_only']:
                    Lists = {}
                    Lists['left'] = left_list[-2:]
                    Lists['right'] = right_list[-2:]##

                #cy("line 494")
                if N['lidar_only']:
                    for side in ['left','right']:
                        advance(rLists[side], zeros((net_input_height,net_input_width,3),np.uint8), 4 )
                else:
                    for side in ['left','right']:
                        for i in [-1]:#,-2]:
                            advance(rLists[side], cv2.resize(Lists[side][i],(net_input_width,net_input_height)), 4 )


                if len(rLists['left'])>2:
                    #cy("if len(rLists['left'])>2:")
                    if N['use LIDAR']:
                        if len(rLists['left']) >= 2:
                            if N['use LIDAR']:
                                #cy("if N['use LIDAR']:")
                                if len(lidar_list) > 4:
                                    #print len(lidar_list)
                                    rLists['left'][-2][:,:,1] = lidar_list[-1]
                                    rLists['left'][-2][:,:,2] = lidar_list[-2]

                                    rLists['right'][-2][:,:,1] = lidar_list[-3]
                                    rLists['right'][-2][:,:,2] = lidar_list[-4]
                            #else print len(lidar_list)
                                #so(rLists,opjD('rLists'))
                                #raw_enter()

                                #print shape(rLists['left'][0]), shape(rLists['right'][0])
                                #mi(rLists['left'][0],0)
                                #mi(rLists['left'][1],1)
                                #mi(rLists['right'][0],10)
                                #mi(rLists['right'][1],11)
                                #spause()
                            
                            #print Durations[dname]['timer'].time()
                            #Durations[dname]['list'].append(1000.0*Durations[dname]['timer'].time())
                            #Durations[dname]['timer'].reset()
                            #cr('D')
                    if N['show_net_input']:# in Arguments:
                        #cy("N['show_net_input']")                
                        if True:#'show_net_input' in ppc.A:
                            if True:#ppc.A['show_net_input']:
                                if even:
                                    l0 = rgbcat(rLists,'left',-1)
                                    ln1 = rgbcat(rLists,'left',-2)
                                    r0 = rgbcat(rLists,'right',-1)
                                    rn1 = rgbcat(rLists,'right',-2)
                                    l = tcat(l0,ln1)
                                    r = tcat(r0,rn1)
                                    lr = lrcat(l,r)
                                    mci((z2o(lr)*255).astype(np.uint8),scale=1.0,color_mode=cv2.COLOR_GRAY2BGR,title='ZED')
                                    even = False
                                else:
                                    even = True
                    #cr('E')


                    

            
            
            #cr('F')
    

            ##
            ####################################################
            ####################################################
            ####################################################
            #dname = 'torch camera format'
            #Durations[dname]['timer'].reset()
            #'fuse images','torch camera format','run mode']



            if len(rLists['left'])>2:
                #cy("if len(rLists['left'])>2:")
            # if len(left_list) > nframes + 2:
                #print shape(rLists['left'])
                #print shape(rLists['right'])
                camera_data = Torch_network['format_camera_data__no_scale'](rLists['left'],rLists['right'])
                #print camera_data #1 12 94 168 as should be: 1x12x94x168
                
                #Durations[dname]['list'].append(1000.0*Durations[dname]['timer'].time())
                #if first_time:
                if behavioral_mode not in Metadata_tensors.keys():
                    for j in range(10):
                        cs("ERROR!!!!!!!!!!!!!!!!!!!!!!")
                    cr("behavioral_mode",behavioral_mode,"not in Metadata_tensors.keys()")
                if behavioral_mode in Metadata_tensors:
                    metadata = Metadata_tensors[behavioral_mode]
                else:
                    cr("*** Warning, behavioral_mode '",behavioral_mode,"'is not in Metadata_tensors using workaround. ***")
                    metadata = Torch_network['format_metadata']((direct,follow,furtive,play,left,right)) #((right,left,play,furtive,follow,direct))
                #    first_time = False
                #dname = 'torch camera format'
                #Durations[dname]['timer'].reset()

                torch_motor_prev, torch_steer_prev = torch_motor, torch_steer

                torch_motor, torch_steer = Torch_network['run_model'](camera_data, metadata, N)

                if np.abs(torch_steer - torch_steer_prev) > N['camera_move_threshold']:
                    torch_camera = torch_steer

                #Durations[dname]['list'].append(1000.0*Durations[dname]['timer'].time())
                
                #Torch_network['output'] should contain full output array of network
                
                #cr('G')


                #s1_flex = N['network_motor_smoothing_parameter']
                #s2_flex = N['network_servo_smoothing_parameter']

                if 'new position for flex insert':
                    if False:#N['use flex'] and flex_motor < 47:
                        torch_steer = flex_steer
                        torch_motor = flex_motor
                        sm = N['flex_motor_smoothing_parameter']
                        ss = N['flex_servo_smoothing_parameter']
                        gm = N['flex_motor_gain']
                        gs = N['flex_steer_gain']
                        
                        cr(int(torch_steer),int(torch_motor),gm)
                    else:
                        sm = N['network_motor_smoothing_parameter']
                        ss = N['network_servo_smoothing_parameter']
                        if torch_motor >= 49:
                            gm = N['network_motor_gain']
                        else:
                            gm = N['network_reverse_motor_gain']
                        gs = N['network_steer_gain']
                        
                        cg(int(torch_steer),int(torch_motor))
                        
                gc = N['network_camera_gain']          
                sc = N['network_camera_smoothing_parameter']

                if 'Do smoothing of percents...':
                    current_camera = (1.0-sc)*torch_camera + sc*current_camera
                    current_steer = (1.0-ss)*torch_steer + ss*current_steer
                    current_motor = (1.0-sm)*torch_motor + sm*current_motor



                #cr('H')
                adjusted_motor = int(gm*(current_motor-49) + N['network_motor_offset'] + 49)
                adjusted_steer = int(gs*(current_steer-49) + 49)
                adjusted_camera = int(gc*(current_camera-49) + 49)

                adjusted_motor = bound_value(adjusted_motor,0,99)
                adjusted_steer = bound_value(adjusted_steer,0,99)
                adjusted_camera = bound_value(adjusted_camera,0,99)

                adjusted_motor = min(adjusted_motor,N['max motor'])
                adjusted_motor = max(adjusted_motor,N['min motor'])


                if True:#not 'original position for flex insert':
                    if N['use flex'] and flex_motor < 47:
                        #adjusted_camera = flex_steer

                        adjusted_steer = N['flex_steer_gain']*(flex_steer-49)+49
                        adjusted_steer = bound_value(adjusted_steer,0,99)
                        adjusted_motor = flex_motor
                        cr(adjusted_camera,adjusted_steer,adjusted_motor)
                    else:
                        cg(int(torch_steer),int(torch_motor))
                            #adjusted_camera,adjusted_steer,adjusted_motor)

                frequency_timer.freq(name='network',do_print=True)

                #if N['camera_auto_zero_for_small_values_int'] > 0:
                if np.abs(adjusted_camera-49) < N['camera_auto_zero_for_small_values_int']:
                    adjusted_camera = 49


                #cr('I')
                camera_cmd_pub.publish(std_msgs.msg.Int32(adjusted_camera))
                steer_cmd_pub.publish(std_msgs.msg.Int32(adjusted_steer))
                motor_cmd_pub.publish(std_msgs.msg.Int32(adjusted_motor))
                


                if N['show_net_activity']:
                    #cy["if N['show_net_activity']:"]
                    if show_timer.check():
                        ############################
                        Net_activity = Activity_Module.Net_Activity('batch_num',0, 'activiations',Torch_network['solver'].A)
                        #Net_activity['view']('moment_index',i,'delay',33, 'scales',{'camera_input':4,'pre_metadata_features':0,'pre_metadata_features_metadata':1,'post_metadata_features':2})
                        ############################
                        show_timer.reset()



                if show_durations.check():

                    for d in durations:
                        pass
                        #cg(d,':',dp(np.median(Durations[d]['list']),1),'ms')
                        #print len(left_list)
                        #print len(rLists['left'])
                    show_durations.reset()
            else:
                cr(len(rLists['left']))

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

    else:
        time.sleep(0.00001)

CS_('goodbye!',__file__)
CS_("doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))")
time.sleep(0.01)
unix(opjh('kzpy3/scripts/kill_ros.sh'))
#default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)



#EOF

    