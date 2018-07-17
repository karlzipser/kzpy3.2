from kzpy3.utils2 import *



Int = 'std_msgs.msg.Int32'
Rostopics = {'/bair_car/cmd/steer':{'type':Int},
    '/bair_car/cmd/motor':{'type':Int}
    }

callback_strs = []
subscriber_strs = []
for name in Rostopics.keys():
    if 'extra' in Rostopics[name].keys():
        extra = Rostopics[name]['extra']
    else:
        extra = ''
    callback_name = 'callback_'+get_safe_name(name)
    callback_strs.append(d2n("def ",callback_name,"(msg):",extra,"\n\tP['",name,"'] = msg\n"))
    subscriber_strs.append(d2n("rospy.Subscriber('",name,"', ",Rostopics[name]['type'],", callback=",callback_name,')\n'))

rospyinit_str = "rospy.init_node('rostopics',anonymous=True)"

print "\n################\n#"
print rospyinit_str
for c in callback_strs:
    print c
for s in subscriber_strs:
    print s
print "#\n################"

P = {}
P['cmd/steer'] = 0
if using_linux():
    ################
    #
    import std_msgs.msg
    import geometry_msgs.msg
    import rospy
    ################
    #
    rospy.init_node('rostopics',anonymous=True)
    def callback__bair_car_cmd_motor(msg):
        P['/bair_car/cmd/motor'] = msg

    def callback__bair_car_cmd_steer(msg):
        P['/bair_car/cmd/steer'] = msg

    rospy.Subscriber('/bair_car/cmd/motor', std_msgs.msg.Int32, callback=callback__bair_car_cmd_motor)

    rospy.Subscriber('/bair_car/cmd/steer', std_msgs.msg.Int32, callback=callback__bair_car_cmd_steer)

    #
    ################

    timer = Timer(0.2)
    timer2 = Timer()
    while timer2.time() < 10:
        #print timer2.time()
        timer.message(d2s("cmd/steer =",P['cmd/steer']))



