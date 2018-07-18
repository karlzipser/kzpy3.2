from kzpy3.utils2 import *

Int = 'std_msgs.msg.Int32'
Float = 'std_msgs.msg.Float32'
Vec3 = 'geometry_msgs.msg.Vector3'
Str = 'std_msgs.msg.String'
B = '/bair_car/'

Rostopics_subscribe = [
    ('steer',Int),
    ('motor',Int),
    ('cmd/steer',Int),
    ('cmd/motor',Int),
    ('network_servo_percent',Int),
    ('network_motor_percent',Int),  
    ('human_agent',Int),
    ('behavioral_mode',Str),
    ('button_number',Int),
    ('drive_mode',Int),
    ('encoder',Float),
    ('gyro',Vec3),
    ('gyro_heading',Vec3),
    ('acc',Vec3),
    ('Hz_acc',Float),
    ('Hz_mse',Float),
    ('Hz_network',Float)
    ]
Rostopics_publish = [('network_smoothing_parameter',Float),
    ('network_output_sample',Int),
    ('network_motor_offset',Int),
    ('network_steer_gain',Float),
    ('network_motor_gain',Float)
    ]

def get_ros_subscriber_strs(Rostopics_subscribe):
    callback_strs = []
    subscriber_strs = []
    P_subscribe_strs = ['P = {}']
    for topic in Rostopics_subscribe:
        name = B+topic[0]
        callback_name = 'callback_'+get_safe_name(name)
        if topic[1] == Vec3:
            callback_strs.append(d2n("def ",callback_name,"(msg):","\n\tP['",name,"'] = (msg.x,msg.y,msg.z)\n"))
        else:
            callback_strs.append(d2n("def ",callback_name,"(msg):","\n\tP['",name,"'] = msg.data\n"))
        subscriber_strs.append(d2n("rospy.Subscriber('",name,"', ",topic[1],", callback=",callback_name,')\n'))
        P_subscribe_strs.append(d2n("P['",name,"'] = 0"))
    rosimport_str = "import std_msgs.msg\nimport geometry_msgs.msg\nimport rospy"
    rospyinit_str = "rospy.init_node('rostopics',anonymous=True)"
    return rosimport_str,rospyinit_str,P_subscribe_strs,callback_strs,subscriber_strs




def get_ros_publisher_strs(Rostopics_publish,P):
    pub_setup_strs = []
    pub_publish_strs = []
    P_publisher_strs = {}
    for topic in Rostopics_publish:
        
        name = topic[0]
        P[B+name] = 0
        rtype = topic[1]
        pub_name = get_safe_name(name)+'_pub'
        pub_setup_strs.append(d2n(pub_name," = rospy.Publisher('",name,"', ",rtype,", queue_size=100)"))
        pub_publish_strs.append(d2n(pub_name,".publish(",rtype,"(",P[B+name],")"))
    return pub_setup_strs,pub_publish_strs




rosimport_str,rospyinit_str,P_subscribe_strs,callback_strs,subscriber_strs = get_ros_subscriber_strs(Rostopics_subscribe)
#exec_ros_subscriber_strs(rosimport_str,rospyinit_str,P_subscribe_strs,callback_strs,subscriber_strs)


print "\n################\n#"
if using_linux(): exec(rosimport_str)
print rosimport_str
if using_linux(): exec(rospyinit_str)
print rospyinit_str
for p in P_subscribe_strs:
    if using_linux(): exec(p)
    print p
for c in callback_strs:
    if using_linux(): exec(c)
    print c
for s in subscriber_strs:
    if using_linux(): exec(s)
    print s
print "#\n################"



pub_setup_strs,pub_publish_strs = get_ros_publisher_strs(Rostopics_publish,P)
#exec_pub_setup_strs(pub_setup_strs)
#exec_pub_publish_strs(pub_publish_strs)



#def exec_ros_subscriber_strs(rosimport_str,rospyinit_str,P_subscribe_strs,callback_strs,subscriber_strs):




#def exec_pub_setup_strs(pub_setup_strs):
print "\n################\n#"
for p in pub_setup_strs:
    if using_linux(): exec(p)
    print p
print "#\n################"
#def exec_pub_publish_strs(pub_publish_strs):
print "\n################\n#"
for c in pub_publish_strs:
    if using_linux(): exec(c)
    print c
print "#\n################"

raw_enter()



#steer_cmd_pub = rospy.Publisher('cmd/steer', std_msgs.msg.Int32, queue_size=100)
#steer_cmd_pub.publish(std_msgs.msg.Int32(adjusted_steer))
def get_bag_info():
    try:
        latest_rosbag_folder = most_recent_file_in_folder(opjm('rosbags'))
        latest_rosbag = most_recent_file_in_folder(latest_rosbag_folder)
        bag_num = fname(latest_rosbag).split('_')[-1]
        bag_time = os.path.getmtime(latest_rosbag)
        bag_time = int( time.time() - bag_time)
        bag_size = os.path.getsize(latest_rosbag)
        bag_size = dp(bag_size/1000000000.)
        return_str = d2s(bag_num,bag_size,'GB',bag_time,'s',time_str('TimeShort'))
        return return_str
    except:
        return 'rosbags not found or other problem'


bag_timer = Timer(5)
bag_str = ''
while True:
    ctr = 0
    time.sleep(0.1)
    print(chr(27) + "[2J")
    for topic in Rostopics_subscribe:
        val = P[B+topic[0]]
        if is_number(val):
            val = dp(val,2)
        pd2s(topic[0],"=\t",val)
        ctr += 1
        if bag_timer.check():
            bag_str = get_bag_info()
            bag_timer.reset()
    print bag_str
            
"""
USE_CURSES = False
if using_linux():
    exec(rosimport_str)
    exec(rospyinit_str)
    for p in P_subscribe_strs:
        exec(p)
    for c in callback_strs:
        exec(c)
    for s in subscriber_strs:
        exec(s)   
    timer = Timer(0.01)
"""
print 'done.'

