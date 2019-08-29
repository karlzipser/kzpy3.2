#!/usr/bin/env python
from kzpy3.vis3 import *
assert HAVE_ROS

setup_Default_Arguments(
    {
        'seconds':3600,
        'scale':1,
        'delay':33,
        'topic':"/bair_car/zed/left/image_rect_color",
        'help':0,
        'save_samples':False,
    }
)
print_Arguments()

import roslib
import std_msgs.msg
import geometry_msgs.msg
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
exec(identify_file_str)
bridge = CvBridge()

ROS_initalized = False

image_list = []




def image_callback(data):
    global image_list
    cimg = bridge.imgmsg_to_cv2(data,"rgb8")
    if len(image_list) > 2 + 3:
        image_list = image_list[-(2 + 3):]
    image_list.append(cimg)





def action(topic,scale=1,delay=33,s=3600,save_samples=False):
    global ROS_initalized
    if not ROS_initalized:
        rospy.Subscriber(topic,Image,image_callback,queue_size = 1)
        rospy.init_node('show_image_from_ros_'+str(np.random.randint(1000000)),anonymous=True)
        ROS_initalized = True

    main_timer = Timer(s)

    waiting = Timer(1)

    save_samples_timer = Timer(1)

    samples_dir = opjD(d2n(topic,'.',time.time()))

    os.system(d2s('mkdir -p',samples_dir))

    ctr = 0

    first_time = True

    while not main_timer.check():

        if len(image_list) > 2:
            img = image_list[-1]
            if first_time:
                first_time = False
                pd2s(topic,"image shape =",shape(img))
            if save_samples_timer.check():
                save_samples_timer.reset()
                imsave(opj(samples_dir,d2n(ctr,'.png')),img)
            ctr += 1
            #mi(img);spause()
            q = mci(img,delay=33,title=topic,scale=scale)
            if q == ord('q'):
                sys.exit()
        else:
            waiting.message('waiting for data...')






if __name__ == '__main__':

    action(
        Arguments['topic'],
        Arguments['scale'],
        Arguments['delay'],
        Arguments['seconds'],
        Arguments['save_samples'],
    )

    cb('\nDone.\n')
#EOF

    

