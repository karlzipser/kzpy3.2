#!/usr/bin/env python
from kzpy3.vis3 import *
exec(identify_file_str)

import rospy
import torch
import roslib
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
bridge = CvBridge()
import cv2

ga = getattr
sa = setattr

class C:
    def __init__(self):
        pass


class CameraShot:
    def __init__(self,data):
        self.img = bridge.imgmsg_to_cv2(data,'rgb8')
        self.ts = data.header.stamp.secs + data.header.stamp.nsecs / 10.0**9
        self.seq = data.header.seq


class Quartet:
    def __init__(self):
        self.left_now   = None
        self.right_now  = None
        self.left_prev  = None
        self.right_prev = None
    def display(self):
        img_now = np.zeros((94,2*168+10,3),np.uint8)
        img_prev = np.zeros((94,2*168+10,3),np.uint8)
        img_now[:,:168,:] = self.right_now
        img_now[:,-168:,:] = self.left_now
        img_prev[:,:168,:] = self.right_prev
        img_prev[:,-168:,:] = self.left_prev

        mci(img_prev,scale=4,delay=10,title='1')
        mci(img_now,scale=4,delay=1,title='1')


D={}
D['call'] = 0
D['success'] = 0
D['fail 1'] = 0
D['fail 2'] = 0
D['fail 3'] = 0

Zed = C()
Zed.left = []
Zed.right = []

L = {}
L['left_ready'] = False

def zed_lst_lim(zed,side,max_len,min_len):
    l = ga(zed,side)
    if len(l) > max_len:
        sa(zed,side,l[-min_len:])

dt_left_lst = []
dt_right_lst = []
dt_now_lst = []

def build_quartet():
    D['call'] += 1
    try:
        for i in [-1,-2,-3]:
            dt_now = Zed.left[i].ts - Zed.right[-1].ts
            if dt_now > -0.01 and dt_now < 0.02:
                break
        else:
            D['fail 3']+=1
            return None

        dt_left = Zed.left[i].ts - Zed.left[i-1].ts
        
        dt_right = Zed.right[-1].ts - Zed.right[-2].ts
        
        if dt_left > 0.025 and dt_left < 0.04:
            if dt_right > 0.025 and dt_right < 0.04:
                Q = Quartet()
                Q.left_now = Zed.left[i].img
                Q.right_now =  Zed.right[-1].img
                Q.left_prev = Zed.left[i-1].img
                Q.right_prev = Zed.right[-2].img
                D['success']+=1
                dt_left_lst.append(dt_left)
                dt_right_lst.append(dt_right)
                dt_now_lst.append(dt_now)
                return Q
            else:
                D['fail 1']+=1
        else:
            cr('dt_left ',dt_left)
            D['fail 2']+=1
            return None

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
        return None


Hz = {}
Hz['left'] = Timer(1)
Hz['right'] = Timer(1)


def left_callback(data):
    Zed.left.append(CameraShot(data))
    zed_lst_lim(Zed,'left',6,4)
    L['left_ready'] = True


def right_callback(data):
    Zed.right.append(CameraShot(data))
    zed_lst_lim(Zed,'right',6,4)


bcs = '/bair_car'
rospy.init_node('camera',anonymous=True,disable_signals=True)
rospy.Subscriber(
    bcs+"/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber(
    bcs+"/zed/left/image_rect_color",Image,left_callback,queue_size = 1)







if __name__ == '__main__':

    hz = Timer(5)
    print_timer = Tr(5)
    timer = Tr()

    while not rospy.is_shutdown():

        if len(Zed.left) > 3 and L['left_ready']:
            L['left_ready'] = False
            Q = build_quartet()
            if Q == None:
                pass#failure+=1
            else:
                #success+=1
                Q.display()
            hz.freq()
            print_timer.message(
                d2s(D,
                    dp(timer.time()),
                    dp(100*D['success']/(1.0*D['call'])),'%'))










if False:

    figure('dt_now_lst');clf();hist(dt_now_lst,1000)
    figure('dt_left_lst');clf();hist(dt_left_lst)
    figure('dt_right_lst');clf();hist(dt_right_lst)


    for i in range(10):
        if i == 667:
            print 6
            break
    else:
        print 11

    """
    frame_id: /zed_current_frame
    seq: 2839
    stamp: 
      secs: 1544744879
      nsecs: 789260922
    """
#EOF

    