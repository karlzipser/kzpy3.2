from kzpy3.utils2 import *

Int = 'std_msgs.msg.Int32'
Float = 'std_msgs.msg.Float32'
Vec3 = 'geometry_msgs.msg.Vector3'
Str = 'std_msgs.msg.String'

rosimport_str = "import std_msgs.msg\nimport geometry_msgs.msg\nimport rospy"
rospyinit_str = "rospy.init_node('________',anonymous=True)"


def get_ros_publisher_strs(Rostopics_to_publish,R,Values_src_dic,initalize_Rs=False):
    pub_setup_strs = []
    pub_publish_strs = []
    P_publisher_strs = {}
    for topic in Rostopics_to_publish:
        
        name = topic[0]
        if initalize_Rs:
            if name in Values_src_dic.keys():
                R[name] = Values_src_dic[name]
            else:
                R[name] = 0
        rtype = topic[1]
        pub_name = get_safe_name(name)+'_pub'
        pub_setup_strs.append(d2n(pub_name," = rospy.Publisher('",name,"', ",rtype,", queue_size=100)"))
        pub_publish_strs.append(d2n(pub_name,".publish(",rtype,"(",R[name],"))"))
    return pub_setup_strs,pub_publish_strs


Topics = [
    ('network_smoothing_parameter',Float),
    ('network_output_sample',Int),
    ('network_motor_offset',Int),
    ('network_steer_gain',Float),
    ('network_motor_gain',Float),
    ('servo_pwm_smooth_manual_offset',Int)
]

def get_ros_subscriber_strs(Rostopics_subscribe_to):
    subscription_strs = []
    for topic in Rostopics_subscribe_to:
        assert type(topic) == tuple
        assert len(topic) == 2
        raw_name = topic[0]
        safe_name = get_safe_name(raw_name)
        rtype = topic[1]
        subscription_strs.append("""def """+safe_name+"""_callback(msg):\n\tR["""+safe_name+"""] = msg.data\n""")
        subscription_strs.append("""rospy.Subscriber('"""+raw_name+"""',"""+rtype+""", callback="""+safe_name+"""_callback)\n""")
    return subscription_strs

subscription_strs = get_ros_subscriber_strs(Topics)
list_of_strings_to_txt_file(opjh('temp.py'),subscription_strs)

#EOF
