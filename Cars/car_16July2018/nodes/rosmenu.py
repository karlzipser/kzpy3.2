from kzpy3.utils2 import *
P = {}
Int = 'std_msgs.msg.Int32'
Float = 'std_msgs.msg.Float32'
Vec3 = 'geometry_msgs.msg.Vector3'
Str = 'std_msgs.msg.String'

Rostopics_publish = [('network_smoothing_parameter',Float),
    ('network_output_sample',Int),
    ('network_motor_offset',Int),
    ('network_steer_gain',Float),
    ('network_motor_gain',Float)
    ]

rosimport_str = "import std_msgs.msg\nimport geometry_msgs.msg\nimport rospy"
rospyinit_str = "rospy.init_node('rostopics',anonymous=True)"

def get_ros_publisher_strs(Rostopics_publish,P,zero_Ps=False):
    pub_setup_strs = []
    pub_publish_strs = []
    P_publisher_strs = {}
    for topic in Rostopics_publish:
        
        name = topic[0]
        if zero_Ps:
            P[name] = 0
        rtype = topic[1]
        pub_name = get_safe_name(name)+'_pub'
        pub_setup_strs.append(d2n(pub_name," = rospy.Publisher('",name,"', ",rtype,", queue_size=100)"))
        pub_publish_strs.append(d2n(pub_name,".publish(",rtype,"(",P[name],"))"))
    return pub_setup_strs,pub_publish_strs

print "\n################\n#"
if using_linux(): exec(rosimport_str)
print rosimport_str
if using_linux(): exec(rospyinit_str)
print rospyinit_str
print "#\n################"

pub_setup_strs,pub_publish_strs = get_ros_publisher_strs(Rostopics_publish,P,zero_Ps=True)
print "\n################\n#"
for p in pub_setup_strs:
    if using_linux(): exec(p)
    print p
print "#\n################"
print "\n################\n#"
for c in pub_publish_strs:
    if using_linux(): exec(c)
    print c
print "#\n################"


while True:
    pprint(P)
    ctr = 0
    for topic in Rostopics_publish:
        name = topic[0]
        pd2s(ctr,')',name,':',dp(P[name],2))
        ctr += 1
    choice_number = input('choice > ')
    if is_number(choice_number):
        if choice_number < 0:
            continue
        if choice_number+1 > len(Rostopics_publish):
            continue
        choice_number = int(choice_number)
        name = Rostopics_publish[choice_number][0]
        P[name] = input(name+' value > ')
        pub_setup_strs,pub_publish_strs = get_ros_publisher_strs(Rostopics_publish,P)
        print "\n################\n#"
        for c in pub_publish_strs:
            if using_linux(): exec(c)
            print c
        print "#\n################"
        # add exit choice.
print 'done.'

