#!/usr/bin/env python

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

while not rospy.is_shutdown():

    time.sleep(0.001)
    
    if (left_calls > left_calls_prev) and (len(left_list) > nframes + 1):##human_agent == 0 and drive_mode == 1:

        dname = 'fuse images'
        Durations[dname]['timer'].reset()

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
        Lists['right'] = right_list[-2:]##
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


        Durations[dname]['list'].append(1000.0*Durations[dname]['timer'].time())

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


            if show_durations.check():
                for d in durations:
                    cg(d,':',dp(np.median(Durations[d]['list']),1),'ms')
                show_durations.reset()

            

    else:
        pass

    left_calls_prev = left_calls

if __name__ == '__main__':
    rospy.init_node('network_node',anonymous=True,disable_signals=True)
    
#EOF







