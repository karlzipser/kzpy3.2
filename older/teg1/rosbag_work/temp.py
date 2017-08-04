
from kzpy3.vis import *
import rospy
import rosbag
import sensor_msgs.msg
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError
bridge = cv_bridge.CvBridge()

b = opjD("bair_car_data/furtive_9August2016/bags/bair_car_2016-08-09-17-27-34_27.bag")

bag = rosbag.Bag(b)

t0 = time.time()
ctr = 0
for i in range(1024):
    a = 1470788870.0 + 15.0*random.random()
    b = a + .038
    for m in bag.read_messages(topics=['/bair_car/zed/left/image_rect_color'],start_time=rospy.Time.from_sec(a),end_time=rospy.Time.from_sec(b)):
        t = round(m.timestamp.to_time(),3)
        t_str = "%.3f"%t
        #print t
        img = bridge.imgmsg_to_cv2(m[1],"rgb8")
        ctr += 1
t1 = time.time()
rate = (t1-t0)/(1.0*ctr)
print(d2s('rate =',rate,"ctr =",ctr))

ctr2 = 0
t0 = time.time()
fs = glob.glob(opjD('bair_car_data/furtive_9August2016/images/left_image/links/*.png'))
for i in range(1024):
    img = imread(fs[i])
    ctr2 += 1
t1 = time.time()
rate2 = (t1-t0)/(1.0*ctr2)
print(d2s('rate =',rate2))
