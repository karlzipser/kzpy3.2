#!/usr/bin/env python
from kzpy3.vis3 import *
exec(identify_file_str)



import rospy
import torch
import roslib
import cv2
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
bridge = CvBridge()

ga = getattr
sa = setattr

class C:
    def __init__(self):
        pass

Zed = C()
Zed.calls = 0
Zed.success = 0
Zed.fails_1 = 0
Zed.fails_2 = 0
Zed.fails_3 = 0
Zed.fails_4 = 0
Zed.left = []
Zed.right = []
collect_dt_data = False
if collect_dt_data:
    Zed.dt_left_lst = []
    Zed.dt_right_lst = []
    Zed.dt_now_lst = []


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
    Zed.calls += 1
    try:
        for i in [-1,-2,-3]:
            dt_now = Zed.left[i].ts - Zed.right[-1].ts
            if dt_now > -0.01 and dt_now < 0.02:
                break
        else:
            Zed.fails_3+=1
            return None

        dt_left = Zed.left[i].ts - Zed.left[i-1].ts
        dt_right = Zed.right[-1].ts - Zed.right[-2].ts
        
        if dt_left > 0.025 and dt_left < 0.04:
            cg(dt_left,Zed.left[i].seq,Zed.left[i-1].seq)
            if dt_right > 0.025 and dt_right < 0.04:
                Q = Quartet()
                Q.left_now = Zed.left[i].img
                Q.right_now =  Zed.right[-1].img
                Q.left_prev = Zed.left[i-1].img
                Q.right_prev = Zed.right[-2].img
                Zed.success += 1
                if collect_dt_data:
                    Zed.dt_left_lst.append(dt_left)
                    Zed.dt_right_lst.append(dt_right)
                    Zed.dt_now_lst.append(dt_now)
                return Q
            else:
                Zed.fails_1+=1
                return None
        else:
            cr('dt_left ',dt_left,Zed.left[i].seq,Zed.left[i-1].seq)
            Zed.fails_2+=1
            return None

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
        Zed.fails_4 += 1
        return None

def left_callback(data):
    Zed.left.append(CameraShot(data))
    limit_zed_list(Zed,'left',6,4)

def right_callback(data):
    Zed.right.append(CameraShot(data))
    limit_zed_list(Zed,'right',6,4)


bcs = '/bair_car'
rospy.Subscriber(
    bcs+"/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber(
    bcs+"/zed/left/image_rect_color",Image,left_callback,queue_size = 1)

if collect_dt_data:
    def hist_dt_lists():
        figure('Zed.dt_now_lst');clf();hist(Zed.dt_now_lst)
        figure('Zed.dt_left_lst');clf();hist(Zed.dt_left_lst)
        figure('Zed.dt_right_lst');clf();hist(Zed.dt_right_lst)



"""
hz = Timer(10)
print_timer = Tr(10)
timer = Tr()

quartet_list = []

def get_quartet():
    Q = None
    if len(Zed.left) > 3 and Zed.left[-1].ready:
        Zed.left[-1].ready = False
        Q = build_quartet()
        #quartet_list.append((Q,True))

        #if len(quartet_list > 4):
        #    quartet_list = quartet_list[-2:]
        hz.freq()
        print_timer.message(
            d2s(
                dp(timer.time()),
                dp(100*Zed.success/(1.0*Zed.calls)),'%'))
    return Q
"""

#threading.Thread(target=get_quartet,args=[]).start()

















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
                Q.display()#4,1000,1000)
            hz.freq()
            print_timer.message(
                d2s(
                    dp(timer.time()),
                    dp(100*Zed.success/(1.0*Zed.calls)),'%'))
        else:
            time.sleep(1/30./30./30.)



#EOF

    