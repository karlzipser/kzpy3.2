##############################################################
########################    SUBSCRIBE  #######################
###
from kzpy3.vis3 import *
import rospy
import std_msgs.msg
import geometry_msgs.msg
from sensor_msgs.msg import Image
import cv_bridge
bridge = cv_bridge.CvBridge()

S = {}
qs = 1
bcs = '/bair_car/'
var_list_len = 10
S['ts'] = 0
S['ts_prev'] = 0
S['sample_frequency'] = 0
S['gyro_heading_x'] = 0
S['gyro_heading_x_prev'] = 0
S['d_heading'] = 0
S['cmd/motor'] = 49
S['human_agent'] = 49
S['left_image'] = False
S['right_image'] = False
S['delta cmd/camera'] = 0
S['cmd/camera'] = 49
S['encoder_var'] = []
S['encoder'] = 0
S['acc_x_var'] = []
S['acc_x'] = 0
S['acc_y_var'] = []
S['acc_y'] = 0
S['acc_z_var'] = []
S['acc_z'] = 0

def encoder_callback(data):
    S['encoder'] = data.data
    advance(S['encoder_var'],S['encoder'],var_list_len)
rospy.Subscriber(bcs+'encoder', std_msgs.msg.Float32, callback=encoder_callback,queue_size=qs)

S['human/motor'] = 49
def motor_callback(data):
    S['human/motor'] = data.data
rospy.Subscriber(
    bcs+'motor',
    std_msgs.msg.Int32,
    callback=motor_callback,
    queue_size=qs
)


S['button_number'] = 0
def button_number_callback(data):
    S['button_number'] = data.data
rospy.Subscriber(
    bcs+'button_number',
    std_msgs.msg.Int32,
    callback=button_number_callback,
    queue_size=qs
)



S['human/steer'] = 49
def human_steer_callback(msg):
    S['human/steer'] = msg.data
rospy.Subscriber(
    '/bair_car/steer',
    std_msgs.msg.Int32,
    callback=human_steer_callback
)

def cmd_motor_callback(msg):
    S['cmd/motor'] = msg.data
rospy.Subscriber(
    '/cmd/motor',
    std_msgs.msg.Int32,
    callback=cmd_motor_callback)

def human_agent_callback(data):
    S['human_agent'] = data.data
rospy.Subscriber(
    bcs+'human_agent',
    std_msgs.msg.Int32,
    callback=human_agent_callback)

def cmd_camera_callback(msg):
    S['delta cmd/camera'] = msg.data - S['cmd/camera']
    S['cmd/camera'] = msg.data




def behavioral_mode_callback(msg):
    S['behavioral_mode'] = msg.data
rospy.Subscriber(
    '/behavioral_mode',
    std_msgs.msg.String,
    callback=behavioral_mode_callback)



def gyro_heading_x_callback(data):
    S['gyro_heading_x_prev'] = S['gyro_heading_x']
    S['gyro_heading_x'] = data.x
    S['d_heading'] = 2*(S['gyro_heading_x']-S['gyro_heading_x_prev'])
    S['ts_prev'] = S['ts']
    S['ts'] = time.time()
    S['sample_frequency'] = 1.0 / (S['ts']-S['ts_prev'])
rospy.Subscriber(bcs+'gyro_heading', geometry_msgs.msg.Vector3, callback=gyro_heading_x_callback,queue_size=qs)


def acc_callback(data):
    S['acc_x'] = data.x
    S['acc_y'] = data.y
    S['acc_z'] = data.z
    advance(S['acc_x_var'],S['acc_x'],var_list_len)
rospy.Subscriber(bcs+'acc', geometry_msgs.msg.Vector3, callback=acc_callback,queue_size=qs)



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
