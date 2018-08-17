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
    ('servo_pwm_smooth_manual_offset',Int)
    ]

rosimport_str = "import std_msgs.msg\nimport geometry_msgs.msg\nimport rospy"
rospyinit_str = "rospy.init_node('rosmenu',anonymous=True)"

import default_values

def get_ros_publisher_strs(Rostopics_publish,P,initalize_Ps=False):
    pub_setup_strs = []
    pub_publish_strs = []
    P_publisher_strs = {}
    for topic in Rostopics_publish:
        
        name = topic[0]
        if initalize_Ps:
            if name in default_values.Network.keys():
                P[name] = default_values.Network[name]
            else:
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

pub_setup_strs,pub_publish_strs = get_ros_publisher_strs(Rostopics_publish,P,initalize_Ps=True)
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

message = False
choice_number = 0
while choice_number != 1:
    try:
        print(chr(27) + "[2J")

        ctr = 2
        print '1) exit'
        for topic in Rostopics_publish:
            name = topic[0]
            if topic[1] == Int:
                print d2n(ctr,') ',name,': ',int(P[name]))
            else:
                print d2n(ctr,') ',name,': ',dp(P[name],2))
            ctr += 1
        if message:
            print message
        choice_number = input('#? ')
        if not is_number(choice_number):
            message = "bad option"
            if False:
                """
                elif choice_number < 1:
                    message = "bad option"
                elif choice_number+2 > len(Rostopics_publish):
                message = "bad option"
                """
        elif choice_number == 1:
            pass
        else:
            message = False
            index_number = int(choice_number)-2
            name = Rostopics_publish[index_number][0]
            current_val = P[name]
            val = num_from_str(raw_input(d2n(name,'(',current_val,') new value > ')))
            if is_number(val):
                P[name] = val
                if Rostopics_publish[index_number][1] == Int:
                    P[name] = int(P[name])
        pub_setup_strs,pub_publish_strs = get_ros_publisher_strs(Rostopics_publish,P)
        for c in pub_publish_strs:
            if using_linux(): exec(c)
    except Exception as e:
        print("********** rosmenu Exception ***********************")
        print(e.message, e.args)
#print 'done.'
print(chr(27) + "[2J")
