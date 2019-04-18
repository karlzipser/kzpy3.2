#!/usr/bin/env python
from kzpy3.vis3 import *
exec(identify_file_str)
import roslib
import std_msgs.msg
import geometry_msgs.msg
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
bridge = CvBridge()

Defaults = {'scale':2,'delay':33,'topics':"/bair_car/zed/right/image_rect_color,/bair_car/zed/left/image_rect_color"}
for k in Defaults:
    if k not in Arguments:
        Arguments[k] = Defaults[k]
for k in Arguments:
    if type(Arguments[k]) == str:
        Argk = d2n("'",Arguments[k],"'")
    else:
        Argk = Arguments[k]
    exec_str = d2s(k,'=',Argk)
    cg(exec_str)
    exec(exec_str)

topics = Arguments['topics'].split(',')
cb('topics =')
for t in topics:
    cg(d2n("'",t,"'"))

Images = {}

for i in range(len(topics)):
    topic = topics[i]
    Images[topic] = []
    cb_str = """
def image_callback_NUM(data):
    cimg = bridge.imgmsg_to_cv2(data,"rgb8")
    if len(Images['TOPIC']) > 2 + 3:
        Images['TOPIC'] = Images['TOPIC'][-(2 + 3):]
    Images['TOPIC'].append(cimg)

rospy.Subscriber('TOPIC',Image,image_callback_NUM,queue_size = 1)

    """.replace('NUM',str(i)).replace('TOPIC',topic)
    print cb_str
    exec(cb_str)

rospy.init_node('show_image_from_ros_'+str(np.random.randint(1000000)),anonymous=True)


waiting = Timer(1)

while True:
    img_lst = []
    for t in Images.keys():
        if len(Images[t]) > 2:
            img_lst.append(Images[t][-1])

        else:
            waiting.message('waiting for data...')
            break
    if len(img_lst) == len(Images.keys()):
        img = vis_square2(z55(na(img_lst)),10,127)
        q = mci(img,delay=33,title=t,scale=scale)
        if q == ord('q'):
            sys.exit()



def group_Images(Images,ordered_keys,padval=127):
    max_s = [0,0]
    img_lst = []
    for k in ordered_keys:
        s = shape(Images[k])
        for i in [0,1]:
            if s[i] > max_s[i]:
                max_s[i] = s[i]
    spacer = np.zeros((max_s[0],10,3),np.uint8)#+padval
    ctr = 0
    for k in ordered_keys:
        img = np.zeros((max_s[0],max_s[1],3),np.uint8)+padval
        o = Images[k]
        s = shape(o)
        a = (max_s[0]-s[0])/2
        b = (max_s[1]-s[1])/2
        print k,s,a,b
        print a,a+s[0],b,b+s[1],shape(o)
        print shape(img)
        img[a:a+s[0],b:b+s[1],:] = o
        img_lst.append(img)
        ctr += 1
        if ctr < len(ordered_keys):
            img_lst.append(spacer)
    mi(np.concatenate(img_lst,1),'group')
    spause()
        #raw_enter()



def group_Images(Images,ordered_keys,padval=127):
    max_s = [0,0]
    img_lst = []
    for k in ordered_keys:
        s = shape(Images[k])
        for i in [0,1]:
            if s[i] > max_s[i]:
                max_s[i] = s[i]
    spacer = np.zeros((max_s[0],10,3),np.uint8)+padval
    ctr = 0
    for k in ordered_keys:
        
        o = Images[k]
        s = shape(o)
        img = np.zeros((max_s[0],s[1],3),np.uint8)+padval
        a = (max_s[0]-s[0])/2
        #b = (max_s[1]-s[1])/2
        print k,s,a,b
        print a,a+s[0],b,b+s[1],shape(o)
        print shape(img)
        img[a:a+s[0],:,:] = o
        img_lst.append(img)
        ctr += 1
        if ctr < len(ordered_keys):
            img_lst.append(spacer)
    mi(np.concatenate(img_lst,1),'group')
    spause()
        #raw_enter()



cb('\nDone.\n')
#EOF

    

