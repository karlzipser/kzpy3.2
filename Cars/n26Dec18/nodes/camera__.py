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
        if shape(self.img)[0] > 94:
            self.img = cv2.resize(self.img,(168,94))

        self.ts = data.header.stamp.secs + data.header.stamp.nsecs / 10.0**9
        self.seq = data.header.seq


    
class Quartet:

    def __init__(self):
        self.left_now   = None
        self.right_now  = None
        self.left_prev  = None
        self.right_prev = None
        self.ready = True

    def display(self,delay1,delay2,scale=4):
        img_now = np.zeros((94,2*168+10,3),np.uint8)
        img_prev = np.zeros((94,2*168+10,3),np.uint8)
        img_now[:,:168,:] = self.right_now
        img_now[:,-168:,:] = self.left_now
        img_prev[:,:168,:] = self.right_prev
        img_prev[:,-168:,:] = self.left_prev
        mci(img_prev,scale=scale,delay=delay1,title='1')
        mci(img_now,scale=scale,delay=delay2,title='1')
    """
    def get_2d_images_as_array(self,a=['left','right'],b=['_now','_prev'],c=[0,1,2]):
        lst = []
        word_lst = []
        for side in ['left','right']:
            for when in ['_now','_prev']:
                for color in [0,1,2]:
                    lst.append(ga(self,side+when)[:,:,color])
                    word_lst.append((side+when,color))
        return na(lst),word_lst
    """

D={}
D['call'] = 0
D['success'] = 0
D['fail a'] = 0
D['fail b'] = 0
D['fail c'] = 0

Zed = C()
Zed.left = []
Zed.right = []

L = {}
L['left_ready'] = False

#dt_left_lst = []
#dt_right_lst = []
#dt_now_lst = []

meta_width,meta_height = 41,23

def zed_lst_lim(zed,side,max_len,min_len):
    l = ga(zed,side)
    if len(l) > max_len:
        sa(zed,side,l[-min_len:])


def build_quartet():
    D['call'] += 1
    if True:#try:
        for i in [-1,-2,-3]:
            dt_now = Zed.left[i].ts - Zed.right[-1].ts
            if dt_now > -0.01 and dt_now < 0.02:
                break
        else:
            D['fail c']+=1
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
                Q.left_now_meta = cv2.resize(Q.left_now,(meta_width,meta_height))
                Q.right_now_meta = cv2.resize(Q.right_now,(meta_width,meta_height))
                Q.left_prev_meta = cv2.resize(Q.left_prev,(meta_width,meta_height))
                Q.right_prev_meta = cv2.resize(Q.right_prev,(meta_width,meta_height))
                D['success']+=1
                #dt_left_lst.append(dt_left)
                #dt_right_lst.append(dt_right)
                #dt_now_lst.append(dt_now)
                return Q
            else:
                D['fail a']+=1
        else:
            #cr('dt_left ',dt_left)
            D['fail b']+=1
            return None

    else:#except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
        return None





def left_callback(data):
    Zed.left.append(CameraShot(data))
    zed_lst_lim(Zed,'left',6,4)
    L['left_ready'] = True


def right_callback(data):
    Zed.right.append(CameraShot(data))
    zed_lst_lim(Zed,'right',6,4)


bcs = '/bair_car'

rospy.Subscriber(
    bcs+"/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber(
    bcs+"/zed/left/image_rect_color",Image,left_callback,queue_size = 1)




QUIT = False

def maintain_quartet_list(Q_list):

    hz = Timer(60)
    print_timer = Tr(60)
    timer = Timer()
    
    while not rospy.is_shutdown() and QUIT == False:

        if len(Zed.left) > 3 and L['left_ready']:

            L['left_ready'] = False
            Q = build_quartet()
            if Q != None:
                Q_list.append(Q)
            while len(Q_list) > 3:
                Q_list.pop(0)
            hz.freq()
            print_timer.message(
                d2s(D,
                    dp(timer.time()),
                    dp(100*D['success']/(1.0*D['call'])),'%'))
        else:
            time.sleep(1/10000.)

    cg('\nExiting maintain_quartet_list thread.\n')


Q_list = []

threading.Thread(target=maintain_quartet_list,args=[Q_list]).start()


if __name__ == '__main__':
    rospy.init_node('camera',anonymous=True,disable_signals=True)

    hz = Timer(30)
    wait = Timer()
    wait2 = Timer(30)
    while True:
        if wait.time() > 10:
            if wait2.check():
                cr('wait.time() =',int(wait.time()))
                wait2.reset()
        try:
            if len(Q_list) > 0:
                if Q_list[-1].ready:
                    Q_list[-1].ready = False
                    Q_list[-1].display(1,1,4)
                    hz.freq(' (main) ')
                    wait.reset()
                    continue
            time.sleep(1./10000.)
    
        except KeyboardInterrupt:
            QUIT = True
            cr('\n\n*** KeyboardInterrupt ***\n')
            time.sleep(1)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            #QUIT = True
            #cr('\n\n*** Exception ***\n')
            #time.sleep(1)
    

#EOF

    