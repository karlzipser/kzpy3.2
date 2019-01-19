#!/usr/bin/env python
from kzpy3.vis3 import *
exec(identify_file_str)

ga = getattr
sa = setattr

class C:
    def __init__(self):
        pass

import rospy
import torch
import roslib
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
bridge = CvBridge()
import cv2

S = C()
S.calls = 0
S.success = 0
S.fails_1 = 0
S.fails_2 = 0
S.fails_3 = 0
S.fails_4 = 0


Dt = C()
Dt.left_lst = []
Dt.right_lst = []
Dt.now_lst = []

Zed = C()
Zed.left = []
Zed.right = []


def hist_dt_lists():
    figure('Dt.now_lst');clf();hist(Dt.now_lst)
    figure('Dt.left_lst');clf();hist(Dt.left_lst)
    figure('Dt.right_lst');clf();hist(Dt.right_lst)


class CameraShot:
    def __init__(self,data):
        self.img = bridge.imgmsg_to_cv2(data,'rgb8')
        self.ts = data.header.stamp.secs + data.header.stamp.nsecs / 10.0**9
        self.seq = data.header.seq
        self.ready = True


class Quartet:
    def __init__(self):
        self.left_now   = None
        self.right_now  = None
        self.left_prev  = None
        self.right_prev = None
    def display(self,scale=4,delay1=10,delay2=1):
        img_now = np.zeros((94,2*168+10,3),np.uint8)
        img_prev = np.zeros((94,2*168+10,3),np.uint8)
        img_now[:,:168,:] = self.right_now
        img_now[:,-168:,:] = self.left_now
        img_prev[:,:168,:] = self.right_prev
        img_prev[:,-168:,:] = self.left_prev
        mci(img_prev,scale=scale,delay=delay1,title='Quartet')
        mci(img_now,scale=scale,delay=delay2,title='Quartet')


def limit_zed_list(zed,side,max_len,min_len):
    l = ga(zed,side)
    if len(l) > max_len:
        sa(zed,side,l[-min_len:])


def build_quartet():
    S.calls += 1
    try:
        for i in [-1,-2,-3]:
            dt_now = Zed.left[i].ts - Zed.right[-1].ts
            if dt_now > -0.01 and dt_now < 0.02:
                break
        else:
            S.fails_3+=1
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
                S.success + =1
                Dt.left_lst.append(dt_left)
                Dt.right_lst.append(dt_right)
                Dt.now_lst.append(dt_now)
                return Q
            else:
                fails_1+=1
                return None
        else:
            cr('dt_left ',dt_left)
            S.fails_2+=1
            return None

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
        S.fails_4 += 1
        return None

def left_callback(data):
    Zed.left.append(CameraShot(data))
    limit_zed_list(Zed,'left',6,4)

def right_callback(data):
    Zed.right.append(CameraShot(data))
    limit_zed_list(Zed,'right',6,4)



if __name__ == '__main__':

    bcs = '/bair_car'
    rospy.init_node('camera',anonymous=True,disable_signals=True)
    rospy.Subscriber(
        bcs+"/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
    rospy.Subscriber(
        bcs+"/zed/left/image_rect_color",Image,left_callback,queue_size = 1)

    hz = Timer(5)
    print_timer = Tr(5)
    timer = Tr()

    while not rospy.is_shutdown():

        if len(Zed.left) > 3 and Zed.left[-1].ready:
            # consider Zed.right version of above
            Zed.left[-1].ready = False
            Q = build_quartet()
            if Q != None:
                Q.display()
            hz.freq()
            print_timer.message(
                d2s(D,
                    dp(timer.time()),
                    dp(100*success/(1.0*calls)),'%'))



#EOF

    