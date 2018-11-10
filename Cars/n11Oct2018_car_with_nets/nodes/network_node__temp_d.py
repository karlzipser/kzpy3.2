#!/usr/bin/env python

if 'Torch_network' not in locals():

    from kzpy3.vis3 import *
    exec(identify_file_str)
    sbpd2s("network_node.py")

    import kzpy3.Cars.n11Oct2018_car_with_nets.nodes.Default_values.arduino.default_values as default_values
    N = default_values.P

    import rospy
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
    lidar_list = []



    nframes = 2 #figure out how to get this from network

    left_calls = 0
    left_calls_prev = 0

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

    rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
    rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)






from kzpy3.utils3 import *
import torch
import torch.nn as nn
from torch.autograd import Variable
exec(identify_file_str)
import rospy

spd2s("!!!!! note: from nets.SqueezeNet_ import SqueezeNet !!!!");time.sleep(3)

def Torch_Network(N):
    try:
        D = {}
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
                listoftensors.append(torch.from_numpy(side[-i - 1]))
        camera_data = torch.cat(listoftensors, 2)
        camera_data = camera_data.cuda().float()/255. - 0.5
        camera_data = torch.transpose(camera_data, 0, 2)
        camera_data = torch.transpose(camera_data, 1, 2)
        camera_data = camera_data.unsqueeze(0)
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





##############################################
#
# from kzpy3.vis3 import *

import kzpy3.Data_app.lidar.python_pointclouds6k as ppc

for a in Arguments:
    ppc.A[a] = Arguments[a]

#ppc.rospy.init_node('receive_pointclouds')
ppc.rospy.Subscriber('/os1_node/points', ppc.PointCloud2, ppc.points__callback)

threading.Thread(target=ppc.pointcloud_thread,args=[]).start()
#
##############################################

net_input_width = 168
net_input_height = 94
resize = ppc.resize_versions[0]
image_type = ppc.image_type_versions[0]
mn,mx = -0.5,0.7

waiting = Timer(1)
frequency_timer = Timer(5)

while not rospy.is_shutdown():

    time.sleep(0.001)
    
    if (left_calls > left_calls_prev) and (len(left_list) > nframes + 1):##human_agent == 0 and drive_mode == 1:
        
        frequency_timer.freq(name='network',do_print=True)

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
    
        Lists = {}
        Lists['left'] = left_list[-2:]
        Lists['right'] = right_list[-2:]
        rLists = {}
        rLists['left'] = []
        rLists['right'] = []
        for side in ['left','right']:
            for i in [-1,-2]:
                rLists[side].append( cv2.resize(Lists[side][i],(net_input_width,net_input_height)) )
        
        if len(lidar_list) > 4:
            #print len(lidar_list)
            rLists['left'][-2][:,:,1] = lidar_list[-1]
            rLists['left'][-2][:,:,2] = lidar_list[-2]

            rLists['right'][-2][:,:,1] = lidar_list[-3]
            rLists['right'][-2][:,:,2] = lidar_list[-4]



        if 'show_net_input' in ppc.A:

            if ppc.A['show_net_input']:

                l0 = rgbcat(rLists,'left',-1)
                ln1 = rgbcat(rLists,'left',-2)
                r0 = rgbcat(rLists,'right',-1)
                rn1 = rgbcat(rLists,'right',-2)
                l = tcat(l0,ln1)
                r = tcat(r0,rn1)
                lr = lrcat(l,r)

                mci((z2o(lr)*255).astype(np.uint8),scale=1.0,color_mode=cv2.COLOR_GRAY2BGR,title='ZED')

            

    else:
        time.sleep(0.001)

    left_calls_prev = left_calls



#EOF







