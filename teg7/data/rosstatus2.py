from kzpy3.utils import *
import roslib
import std_msgs.msg
import geometry_msgs.msg
import rospy

steer = 0
def steer_callback(msg):
	global steer
	steer = msg.data

motor = 0
def motor_callback(msg):
	global motor
	motor = msg.data

state = 0
def state_callback(msg):
	global state
	state = msg.data

gyro = (0,0,0)
def gyro_callback(msg):
	global gyro
	gyro = msg

acc = (0,0,0)
def acc_callback(msg):
	global acc
	acc = msg


rospy.init_node('listener',anonymous=True)

rospy.Subscriber('/bair_car/steer', std_msgs.msg.Int32, callback=steer_callback)
rospy.Subscriber('/bair_car/motor', std_msgs.msg.Int32, callback=motor_callback)
rospy.Subscriber('/bair_car/state', std_msgs.msg.Int32, callback=state_callback)
rospy.Subscriber('/bair_car/gyro', geometry_msgs.msg.Vector3, callback=gyro_callback)
rospy.Subscriber('/bair_car/acc', geometry_msgs.msg.Vector3, callback=acc_callback)

timer = Timer(15)

steer_div = 5
motor_div = 5
bag_str = ''
rosbag_folder = most_recent_file_in_folder('/media/ubuntu/rosbags')
bag_files = sgg(opj(rosbag_folder,'*.bag'))
ctr = 0
time.sleep(1)
while not rospy.is_shutdown():

	while(timer.check() == False):
		steer_lst = []
		for i in range(105/steer_div):
			steer_lst.append(' ')
		steer_lst[int(99/2./steer_div)] = '|'
		steer_lst[int(0/2./steer_div)] = '|'
		steer_lst[int(99/1./steer_div)-1] = '|'
		steer_lst[max((99-steer)/steer_div-1,0)] = 'S'
		steer_str = ""
		for s in steer_lst:
			steer_str += s
		
		motor_lst = []
		for i in range(105/motor_div):
			motor_lst.append(' ')
		motor_lst[int(99/2./motor_div)] = '|'
		motor_lst[int(0/2./motor_div)] = '|'
		motor_lst[int(99/1./motor_div)-1] = '|'
		motor_lst[motor/motor_div] = 'M'
		motor_str = ""
		for m in motor_lst:
			motor_str += m

		if ctr >= 5:
			if len(bag_files) > 0:
				bag_str = bag_files[-1].split('_')[-1]
				bag_str += ' Mr_' + rosbag_folder.split('Mr_')[-1]
			ctr = 0
		else:
			bag_str = ""
		ctr += 1

		print(d2s(steer_str,motor_str,state,'[',gyro.x,gyro.y,gyro.y,']','[',acc.x,acc.y,acc.z,']',motor,steer,bag_str))
		time.sleep(0.2)
	rosbag_folder = most_recent_file_in_folder('/media/ubuntu/rosbags')
	bag_files = sgg(opj(rosbag_folder,'*.bag'))
	if len(bag_files) > 0:
		print rosbag_folder.split('/')[-1]
	else:
		print "No bag files saved yet."
	time.sleep(0.2)
	timer.reset()
