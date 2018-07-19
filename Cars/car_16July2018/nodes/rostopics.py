from kzpy3.utils2 import *

Int = 'std_msgs.msg.Int32'
Float = 'std_msgs.msg.Float32'
Vec3 = 'geometry_msgs.msg.Vector3'
Str = 'std_msgs.msg.String'

BC = '/bair_car/'
Rostopics_subscribe = [
    (BC+'steer',Int),
    (BC+'motor',Int),
    (BC+'cmd/steer',Int),
    (BC+'cmd/motor',Int),
    (BC+'network_servo_percent',Int),
    (BC+'network_motor_percent',Int),  
    (BC+'human_agent',Int),
    (BC+'behavioral_mode',Str),
    (BC+'button_number',Int),
    (BC+'drive_mode',Int),
    (BC+'encoder',Float),
    (BC+'gyro',Vec3),
    (BC+'gyro_heading',Vec3),
    (BC+'acc',Vec3),
    (BC+'Hz_acc',Float),
    (BC+'Hz_mse',Float),
    (BC+'Hz_network',Float),
    ('network_output_sample',Int),
    ('network_motor_offset',Int),
    ('network_steer_gain',Float),
    ('network_motor_gain',Float),
    ('network_smoothing_parameter',Float)
    ]

rosimport_str = "import std_msgs.msg\nimport geometry_msgs.msg\nimport rospy"
rospyinit_str = "rospy.init_node('rostopics',anonymous=True)"

def get_ros_subscriber_strs(Rostopics_subscribe):
    callback_strs = []
    subscriber_strs = []
    P_subscribe_strs = ['P = {}']
    for topic in Rostopics_subscribe:
        name = topic[0]
        callback_name = 'callback_'+get_safe_name(name)
        if topic[1] == Vec3:
            callback_strs.append(d2n("def ",callback_name,"(msg):","\n\tP['",name,"'] = (msg.x,msg.y,msg.z)\n"))
        else:
            callback_strs.append(d2n("def ",callback_name,"(msg):","\n\tP['",name,"'] = msg.data\n"))
        subscriber_strs.append(d2n("rospy.Subscriber('",name,"', ",topic[1],", callback=",callback_name,')\n'))
        P_subscribe_strs.append(d2n("P['",name,"'] = 0"))

    return P_subscribe_strs,callback_strs,subscriber_strs


P_subscribe_strs,callback_strs,subscriber_strs = get_ros_subscriber_strs(Rostopics_subscribe)


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
#run for X seconds, then do a raw_enter(), or put in thread and watch for q quit.
raw_enter()
bag_timer = Timer(5)
bag_str = ''

timer = Timer(60*5)
while True:
    if timer.check():
        q = raw_input('q to quit, enter to continue >>')
        if q in ['q','Q']:
            break
        timer.reset()
    ctr = 0
    time.sleep(0.1)
    print(chr(27) + "[2J")
    for topic in Rostopics_subscribe:
        val = P[topic[0]]
        if is_number(val):
            val = dp(val,2)
        pd2s(topic[0],"=\t",val)
        ctr += 1
        if bag_timer.check():
            bag_str = get_bag_info()
            bag_timer.reset()
    print bag_str
            

print 'done.'

