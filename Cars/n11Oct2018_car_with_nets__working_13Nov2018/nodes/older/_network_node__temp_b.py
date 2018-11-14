#!/usr/bin/env python

if 'Torch_network' not in locals():

    from kzpy3.vis3 import *
    exec(identify_file_str)
    sbpd2s("network_node.py")

    import kzpy3.Cars.n11Oct2018_car_with_nets.nodes.Default_values.arduino.default_values as default_values
    N = default_values.P

    import rospy

    #import kzpy3.Cars.n11Oct2018_car_with_nets.nodes.net_utils__temp as net_utils__temp

    import roslib
    import std_msgs.msg
    import geometry_msgs.msg
    import cv2
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

    Hz = 0

    low_frequency_pub_timer = Timer(0.5)

    reverse_timer = Timer(1)
    image_sample_timer = Timer(5)

    node_timer = Timer()

    Torch_network = None

    loaded_net = False

    import kzpy3.Menu_app.menu2 as menu2

    parameter_file_load_timer = Timer(0.5)




#!/usr/bin/env python

from kzpy3.utils3 import *
import torch
import torch.nn as nn
from torch.autograd import Variable
#from nets.SqueezeNet_ import SqueezeNet
exec(identify_file_str)
import rospy

spd2s("!!!!! note: from nets.SqueezeNet_ import SqueezeNet !!!!");time.sleep(3)

def Torch_Network(N):
    try:
        D = {}
        #from kzpy3.Train_app.nets.SqueezeNet40 import SqueezeNet
        D['nframes'] = 2#D['solver'].N_FRAMES
        D['scale'] = nn.AvgPool2d(kernel_size=3, stride=2, padding=1).cuda()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)        
    def _run_model(input,metadata,N):
        D['output'] = D['solver'](input, Variable(metadata))
        torch_motor = 100 * D['output'][0][10+N['network_output_sample']].data[0]
        torch_steer = 100 * D['output'][0][N['network_output_sample']].data[0]
        torch_motor = max(0, torch_motor)
        torch_steer = max(0, torch_steer)
        torch_motor = min(99, torch_motor)
        torch_steer = min(99, torch_steer)
        return torch_motor, torch_steer

    def _format_camera_data(left_list, right_list):
        listoftensors = []
        for i in range(2):
            for side in (left_list, right_list):
                if N['GREY_OUT_TOP_OF_IMAGE']:
                    side[-i - 1][:188,:,:] = 128
                if N['USE_LAST_IMAGE_ONLY']:
                    listoftensors.append(torch.from_numpy(side[-1]))
                else:
                    listoftensors.append(torch.from_numpy(side[-i - 1]))
        camera_data = torch.cat(listoftensors, 2)
        camera_data = camera_data.cuda().float()/255. - 0.5
        camera_data = torch.transpose(camera_data, 0, 2)
        camera_data = torch.transpose(camera_data, 1, 2)
        camera_data = camera_data.unsqueeze(0)
        camera_data = D['scale'](Variable(camera_data))
        camera_data = D['scale'](camera_data)
        return camera_data

    ##################################################################
    #
    def _format_camera_data__no_scale(left_list, right_list):
        listoftensors = []
        for i in range(2):
            for side in (left_list, right_list):
                if N['GREY_OUT_TOP_OF_IMAGE']:
                    side[-i - 1][:188,:,:] = 128
                if N['USE_LAST_IMAGE_ONLY']:
                    listoftensors.append(torch.from_numpy(side[-1]))
                else:
                    listoftensors.append(torch.from_numpy(side[-i - 1]))
        camera_data = torch.cat(listoftensors, 2)
        camera_data = camera_data.cuda().float()/255. - 0.5
        camera_data = torch.transpose(camera_data, 0, 2)
        camera_data = torch.transpose(camera_data, 1, 2)
        camera_data = camera_data.unsqueeze(0)
        #camera_data = D['scale'](Variable(camera_data))
        #camera_data = D['scale'](camera_data)
        return camera_data
    #
    ##################################################################

    def _format_metadata(raw_metadata):
        metadata = torch.FloatTensor()
        ctr = 0
        for mode in raw_metadata:
            metadata = torch.cat((torch.FloatTensor(1, 23, 41).fill_(mode), metadata), 0)
            ctr += 1
        zero_matrix = torch.FloatTensor(1, 23, 41).zero_()
        for i in range(128-ctr):
            metadata = torch.cat((zero_matrix, metadata), 0) 
        return metadata.cuda().unsqueeze(0)

    D['run_model'] = _run_model
    D['format_camera_data'] = _format_camera_data
    D['format_camera_data__no_scale'] = _format_camera_data__no_scale
    D['format_metadata'] = _format_metadata

    return D

Torch_network = Torch_Network(N)




rgb_spacer = zeros((94,2),np.uint8)+128
t_spacer = zeros((4,508),np.uint8)+128
lr_spacer = zeros((200,8),np.uint8)+128


def rgbcat(L,s,t):
    return np.concatenate(( L[s][t][:,:,0],rgb_spacer, L[s][t][:,:,1],rgb_spacer, L[s][t][:,:,2] ),axis=1)
    #return np.concatenate(( L[s][t][:,:,0], L[s][t][:,:,1], L[s][t][:,:,2] ),axis=1)


def tcat(t0,tn1):
    return np.concatenate( (t_spacer,t0,t_spacer,tn1,t_spacer), axis=0)
    #return np.concatenate( (t0,tn1), axis=0)


def lrcat(l,r):
    return np.concatenate( (lr_spacer,l,lr_spacer,r,lr_spacer), axis=1)
    #return np.concatenate( (l,r), axis=1)

##############################################
#
# from kzpy3.vis3 import *

import kzpy3.Data_app.lidar.python_pointclouds6i as ppc

for a in Arguments:
    ppc.A[a] = Arguments[a]

#ppc.rospy.init_node('receive_pointclouds')
ppc.rospy.Subscriber('/os1_node/points', ppc.PointCloud2, ppc.points__callback)

threading.Thread(target=ppc.pointcloud_thread,args=[]).start()
#
##############################################

net_input_width = 168
net_input_height = 94


while not rospy.is_shutdown():

    time.sleep(0.001)
    #Hz = frequency_timer.freq(name='network',do_print=True)

    if True:##human_agent == 0 and drive_mode == 1:
        if len(left_list) > nframes + 2:

            e = []
            Hz = frequency_timer.freq(name='network',do_print=True)
            ##############################################
            #
            # while ppc.A['ABORT'] == False:
            
            if 'd2'  in ppc.Output:
                d2 = ppc.Output['d2']
                shape_ = shape(d2)# == (16,1024)
                #print 'shape_',shape_
                width,height = shape_[0],shape_[1]
                #print 'width',width
                #print 'height',height
                assert width in [512,1024]
                assert height == 16

                half_widths = [int(100*width/360./2),int(180*width/360./2),int(270*width/360./2)]
                # can be moved up if width known

                e = []
                for i in [0,1,2]:
                    half_width = half_widths[i]
                    f = cv2.resize(
                            d2[width/2 - half_width:width/2 + half_width, :],
                            (net_input_height,net_input_width)
                        ).transpose(1,0)
                    f = (255*z2o(f)).astype(int)
                    e.append(f)
                    """
                    mci(
                        (z2o(e[i].transpose(1,0))*255).astype(np.uint8),
                        scale=1.0,
                        color_mode=cv2.COLOR_GRAY2BGR,
                        title=d2s('LIDAR','intensity',int(half_widths[i]*2*360/(1.0*width)),'degrees')
                    )
                    """
                #mi(ppc.Output['e'].transpose(1,0));spause()
                #cr(shape(ppc.Output['e']))
            #cg("pc_main.py")
            #
            ##############################################

            if True: # 600-900 Hz / 395 Hz
                Lists = {}
                Lists['left'] = left_list[-2:]
                Lists['right'] = right_list[-2:]
                rLists = {}
                rLists['left'] = []
                rLists['right'] = []
                for side in ['left','right']:
                    for i in [-1,-2]:
                        rLists[side].append( cv2.resize(Lists[side][i],(net_input_width,net_input_height)) )

                if len(e) == 3:

                    rLists['left'][-2][:,:,1] = e[0]
                    rLists['left'][-2][:,:,2] = e[1]

                    rLists['right'][-2][:,:,1] = e[0]
                    rLists['right'][-2][:,:,2] = e[1]

                    rLists['right'][-1][:,:,1] = e[2]
                    rLists['right'][-1][:,:,2] = e[2]

                l0 = rgbcat(rLists,'left',-1)
                ln1 = rgbcat(rLists,'left',-2)
                r0 = rgbcat(rLists,'right',-1)
                rn1 = rgbcat(rLists,'right',-2)
                l = tcat(l0,ln1)
                r = tcat(r0,rn1)
                lr = lrcat(l,r)
                
                if 'show_net_input' in ppc.A:
                    if ppc.A['show_net_input']:
                        mci((z2o(lr)*255).astype(np.uint8),scale=1.0,color_mode=cv2.COLOR_GRAY2BGR,title='ZED')

            else: # 310 Hz  / 110 Hz
                #camera_data = Torch_network['format_camera_data'](left_list,right_list)
                frequency_timer.freq(name='with scale',do_print=True)

    else:
        time.sleep(0.1)


"""

CS_('goodbye!',__file__)
CS_("doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))")
time.sleep(0.01)
unix(opjh('kzpy3/scripts/kill_ros.sh'))
#default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)


    term 1
    roscore
    term 2
    cd '/home/karlzipser/Desktop/tegra-ubuntu_02Nov18_21h42m51s'
    bags
    term 3
    python kzpy3/Cars/n11Oct2018_car_with_nets/nodes/network_node__temp_b.py

python kzpy3

"""

#EOF







