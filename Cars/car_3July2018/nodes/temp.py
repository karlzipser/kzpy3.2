
import std_msgs.msg
import geometry_msgs.msg
import rospy

P = Parameters
def cmd_steer_callback(msg):
    global P
    P['network']['servo_percent'] = msg.data
def cmd_motor_callback(msg):
    global P
    P['network']['motor_percent'] = msg.data
rospy.init_node('run_arduino',anonymous=True)
rospy.Subscriber('cmd/steer', std_msgs.msg.Int32, callback=cmd_steer_callback)
rospy.Subscriber('cmd/motor', std_msgs.msg.Int32, callback=cmd_motor_callback)
P['human_agent_pub'] = rospy.Publisher('human_agent', std_msgs.msg.Int32, queue_size=5) 
P['behavioral_mode_pub'] = rospy.Publisher('behavioral_mode', std_msgs.msg.String, queue_size=5)
P['button_number_pub'] = rospy.Publisher('button_number', std_msgs.msg.Int32, queue_size=5) 
P['steer_pub'] = rospy.Publisher('steer', std_msgs.msg.Int32, queue_size=5) 
P['motor_pub'] = rospy.Publisher('motor', std_msgs.msg.Int32, queue_size=5) 
P['encoder_pub'] = rospy.Publisher('encoder', std_msgs.msg.Float32, queue_size=5)
P['gyro_pub'] = rospy.Publisher('gyro', geometry_msgs.msg.Vector3, queue_size=100)
P['gyro_heading_pub'] = rospy.Publisher('gyro_heading', geometry_msgs.msg.Vector3, queue_size=100)
P['acc_pub'] = rospy.Publisher('acc', geometry_msgs.msg.Vector3, queue_size=100)

imu_dic = {}
imu_dic['gyro'] = 'gyro_pub'
imu_dic['acc'] = 'acc_pub'
imu_dic['head'] = 'gyro_heading_pub'

def publish_MSE_data(m):
	P[imu_dic[m]].publish(geometry_msgs.msg.Vector3(*P[m]['xyz']))

def publish_MSE_data():
	if P['agent_choice'] == 'human':
	    human_val = 1
	else:
	    human_val = 0
	P['human_agent_pub'].publish(std_msgs.msg.Int32(human_val))            
	P['steer_pub'].publish(std_msgs.msg.Int32(P['human']['servo_percent']))
	P['motor_pub'].publish(std_msgs.msg.Int32(P['human']['motor_percent']))
	P['button_number_pub'].publish(std_msgs.msg.Int32(P['mse']['button_number']))
	P['behavioral_mode_pub'].publish(P['behavioral_mode_choice'])
	P['encoder_pub'].publish(std_msgs.msg.Float32(P['mse']['encoder']))





