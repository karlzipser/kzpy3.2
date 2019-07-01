##############################################################
########################    SUBSCRIBE  #######################
###
from kzpy3.vis3 import *
import rospy
import std_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Image
import default_values
import cv_bridge
bridge = cv_bridge.CvBridge()

S = {}
qs = 1
bcs = '/bair_car/'
S['ts'] = 0
S['ts_prev'] = 0
S['sample_frequency'] = 0
S['gyro_heading_x'] = 0
S['gyro_heading_x_prev'] = 0
S['d_heading'] = 0
S['encoder'] = 0
S['motor'] = 49
S['cmd/motor'] = 49
S['human_agent'] = 49
S['left_image'] = False
S['right_image'] = False
S['delta cmd/camera'] = 0
S['cmd/camera'] = 49

for modality in ['headings','encoders','motors']:
    for side in ['left','direct','right']:
        s = """
def MODALITY_SIDE_callback(data):
    S['MODALITY_SIDE'] = na(data.data).astype(float)/1000.

rospy.Subscriber('/MODALITY_SIDE-TOPIC-SUFFIX', std_msgs.msg.Int32MultiArray, callback= MODALITY_SIDE_callback,queue_size=qs)


        """
        s = s.replace('MODALITY',modality).replace('SIDE',side).replace('-TOPIC-SUFFIX',default_values.P['topic_suffix'])
        exec(s)

def encoder_callback(data):
    S['encoder'] = data.data

def motor_callback(data):
    S['motor'] = data.data

def cmd_motor_callback(msg):
    S['cmd/motor'] = msg.data

def human_agent_callback(data):
    S['human_agent'] = data.data

def cmd_camera_callback(msg):
    S['delta cmd/camera'] = msg.data - S['cmd/camera']
    S['cmd/camera'] = msg.data

rospy.Subscriber(bcs+'encoder', std_msgs.msg.Float32, callback=encoder_callback,queue_size=qs)

rospy.Subscriber(bcs+'motor', std_msgs.msg.Int32, callback=motor_callback,queue_size=qs)

rospy.Subscriber(
    bcs+'human_agent',
    std_msgs.msg.Int32,
    callback=human_agent_callback)

rospy.Subscriber(
    '/cmd/motor',
    std_msgs.msg.Int32,
    callback=cmd_motor_callback)

def behavioral_mode_callback(msg):
    S['behavioral_mode'] = msg.data

rospy.Subscriber(
    '/behavioral_mode',
    std_msgs.msg.String,
    callback=behavioral_mode_callback)

rospy.Subscriber(
    '/bair_car/steer',#'/cmd/camera',
    std_msgs.msg.Int32,
    callback=cmd_camera_callback)

def gyro_heading_x_callback(data):
    S['gyro_heading_x_prev'] = S['gyro_heading_x']
    S['gyro_heading_x'] = data.x
    S['d_heading'] = 2*(S['gyro_heading_x']-S['gyro_heading_x_prev'])
    S['ts_prev'] = S['ts']
    S['ts'] = time.time()
    S['sample_frequency'] = 1.0 / (S['ts']-S['ts_prev'])


rospy.Subscriber(bcs+'gyro_heading', geometry_msgs.msg.Vector3, callback=gyro_heading_x_callback,queue_size=qs)

if default_values.P['graphics 3']:

    def left_callback(data):
        S['left_image'] = bridge.imgmsg_to_cv2(data,'rgb8')
if True:
    def left_callback(data):
        S['left_image'] = bridge.imgmsg_to_cv2(data,'rgb8')
    def right_callback(data):
        S['right_image'] = bridge.imgmsg_to_cv2(data,'rgb8')

    rospy.Subscriber(bcs+"zed/left/image_rect_color",Image,left_callback,queue_size=qs)
    rospy.Subscriber(bcs+"zed/right/image_rect_color",Image,right_callback,queue_size=qs)
###
#####################################################
#####################################################

#EOF
