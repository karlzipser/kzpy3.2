from kzpy3.utils2 import *
P = {}
Int = 'std_msgs.msg.Int32'
Float = 'std_msgs.msg.Float32'
Vec3 = 'geometry_msgs.msg.Vector3'
Str = 'std_msgs.msg.String'

BC = '/bair_car/'

Rostopics_publish = [('network_smoothing_parameter',Float),
    ('network_output_sample',Int),
    ('network_motor_offset',Int),
    ('network_steer_gain',Float),
    ('network_motor_gain',Float),
    (BC+'behavioral_mode',Str),
    (BC+'place_choice',Str)
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

choice_number = 0
while choice_number != -1:
    #pprint(P)
    try:
        print(chr(27) + "[2J")
        ctr = 0
        pd2s(-1,')','quit',':')
        for topic in Rostopics_publish:
            name = topic[0]
            if topic[1] == Int:
                pd2s(ctr,')',name,':',int(P[name]))
            else:
                pd2s(ctr,')',name,':',dp(P[name],2))
            ctr += 1
        choice_number = input('choice > ')
        if not is_number(choice_number):
            pass
        elif choice_number == -1:
            pass
        elif choice_number < 0:
            pass
        elif choice_number+1 > len(Rostopics_publish):
            pass
        else:
            choice_number = int(choice_number)
            name = Rostopics_publish[choice_number][0]
            the_raw_input = raw_input(name+' value > ')
            val = num_from_str(the_raw_input)
            if is_number(val):
                P[name] = val
                #P[name] = input(name+' value > ')
                if Rostopics_publish[choice_number][1] == Int:
                    P[name] = int(P[name])
            else if Rostopics_publish[choice_number][1] == Str:
                    P[name = the_raw_input
        pub_setup_strs,pub_publish_strs = get_ros_publisher_strs(Rostopics_publish,P)
        #print "\n################\n#"
        for c in pub_publish_strs:
            if using_linux(): exec(c)
            #print c
        #print "#\n################"
    except Exception as e:
        print("********** rosmenu Exception ***********************")
        print(e.message, e.args)
print 'done.'

