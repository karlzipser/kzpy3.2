from kzpy3.utils2 import *


def get_ros_setup_str(node_name):
	setup_str = """
#############################################
# Auto-generated ros code
import std_msgs.msg
import geometry_msgs.msg
import rospy

rospy.init_node('NODE_NAME',anonymous=True,disable_signal=True)

# DIC_NAME = {}

def ros_publish(Dic,topic_list):
	for t in topic_list:
		val = Dic[t]['val']
		rtype = Dic[t]['rtype']
		pub = Dic[t]['pub']
		pub.publish(rtype(val))

	"""
	setup_str = setup_str.replace('NODE_NAME',node_name)
	return setup_str

def get_ros_topic_str(raw_name,rtype):
	topic_str = """
DIC_NAME['RAW_NAME'] = {}
def _SAFE_NAME_callback__(msg):
	DIC_NAME['RAW_NAME']['ts'] = time.time()
	DIC_NAME['RAW_NAME']['val'] = msg.data
rospy.Subscriber('RAW_NAME',RTYPE, callback=_SAFE_NAME_callback__)
DIC_NAME['RAW_NAME']['type'] = RTYPE
DIC_NAME['RAW_NAME']['pub'] = rospy.Publisher('RAW_NAME',DIC_NAME['RAW_NAME']['type'], queue_size=5)

	"""
	safe_name = get_safe_name(raw_name)
	topic_str = topic_str.replace('RAW_NAME',raw_name)
	topic_str = topic_str.replace('SAFE_NAME',safe_name)
	topic_str = topic_str.replace('RTYPE',rtype)
	return topic_str

def get_ros_strs(dic_name,Topics):

	ros_setup_str = get_ros_setup_str(node_name='network_node')

	ros_topics_str = ""

	for rtype in Topics:
		for raw_name in Topics[rtype]:
			ros_topics_str += get_ros_topic_str(raw_name,rtype)


	ros_strs = ros_setup_str + ros_topics_str + "\n#\n#############################################"
	ros_strs = ros_strs.replace('DIC_NAME',dic_name)

	return ros_strs


##################

Topics = {
	'std_msgs.msg.Int32':[
    	'/bair_car/servo_feedback',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    ],
    'std_msgs.msg.Float32':[
    	'/bair_car/encoder',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    	'/bair_car/cmd/motor',
    ],
}

ros_strs = get_ros_strs(dic_name='Parameters',Topics=Topics)

text_to_file(opjh('.menu/rostemp.py'),ros_strs)

if False:
	for s in ros_strs.split('\n'):
		exec(s)
	" . . . "
	ros_publish(Parameters,topic_list)








if False:
	import std_msgs.msg
	import geometry_msgs.msg
	import rospy

	rospy.init_node('arduino_node',anonymous=True,disable_signal=True)

	DIC_NAME = {}

	###########################
	#
	def __bair_car_servo_feedback_callback__(msg):
		DIC_NAME['/bair_car/servo_feedback']['ts'] = time.time()
		DIC_NAME['/bair_car/servo_feedback']['val'] = msg.data
	rospy.Subscriber('/bair_car/servo_feedback',rInt, callback=__bair_car_servo_feedback_callback__)
	DIC_NAME['/bair_car/servo_feedback']['type'] = std_msgs.msg.Int32
	DIC_NAME['/bair_car/servo_feedback']['pub'] = rospy.Publisher('/bair_car/servo_feedback',DIC_NAME['/bair_car/servo_feedback']['type'], queue_size=5)
	#
	###########################





	# use . . .
	DIC_NAME['/bair_car/servo_feedback']['pub'](DIC_NAME['/bair_car/servo_feedback']['type'](67))
	# or . . .
	DIC_NAME['/bair_car/servo_feedback']['pub'](67)

	Translation = {
		'/bair_car/cmd/motor':['network','motor'],
	}
	for name in DIC_NAME.keys():
		if name not in Translation.keys():
			tr = name
		else:
			tr = Translation[name]
		if type(tr) == str:
			P[tr] = DIC_NAME[name]['val']
		elif type(tr) == list and len(tr) == 2:
			P[tr[0]][tr[1]] = DIC_NAME[name]['val']
		else:
			CS_(d2s('Translation error with',tr))
			assert False



