from kzpy3.utils2 import *



Int = 'std_msgs.msg.Int32'
Float = 'std_msgs.msg.Float32'

Rostopics = {'/bair_car/steer':{'type':Int},
    #'/bair_car/motor':{'type':Int},
    '/bair_car/encoder':{'type':Float}
    }
callback_strs = []
subscriber_strs = []
P_strs = ['P = {}']
for name in Rostopics.keys():
    if 'extra' in Rostopics[name].keys():
        extra = Rostopics[name]['extra']
    else:
        extra = ''
    callback_name = 'callback_'+get_safe_name(name)
    callback_strs.append(d2n("def ",callback_name,"(msg):",extra,"\n\tP['",name,"'] = msg\n"))
    subscriber_strs.append(d2n("rospy.Subscriber('",name,"', ",Rostopics[name]['type'],", callback=",callback_name,')\n'))
    P_strs.append(d2n("P['",name,"'] = 0"))
rosimport_str = "import std_msgs.msg\nimport geometry_msgs.msg\nimport rospy"
rospyinit_str = "rospy.init_node('rostopics',anonymous=True)"

print "\n################\n#"
print rosimport_str
print rospyinit_str
for p in P_strs:
    print p 
for c in callback_strs:
    print c
for s in subscriber_strs:
    print s
print "#\n################"

if using_linux():
    exec(rosimport_str)
    exec(rospyinit_str)
    for p in P_strs:
        exec(p)
    for c in callback_strs:
        exec(c)
    for s in subscriber_strs:
        exec(s)   
    """ 
    ################
    #
    import std_msgs.msg
    import geometry_msgs.msg
    import rospy
    rospy.init_node('rostopics',anonymous=True)
    P = {}
    P['/bair_car/encoder'] = 0
    P['/bair_car/motor'] = 0
    P['/bair_car/steer'] = 0
    def callback__bair_car_encoder(msg):
        P['/bair_car/encoder'] = msg

    def callback__bair_car_motor(msg):
        P['/bair_car/motor'] = msg

    def callback__bair_car_steer(msg):
        P['/bair_car/steer'] = msg

    rospy.Subscriber('/bair_car/encoder', std_msgs.msg.Float32, callback=callback__bair_car_encoder)

    rospy.Subscriber('/bair_car/motor', std_msgs.msg.Int32, callback=callback__bair_car_motor)

    rospy.Subscriber('/bair_car/steer', std_msgs.msg.Int32, callback=callback__bair_car_steer)

    #
    ################
    """
    timer = Timer(0.2)
    timer2 = Timer()
    while timer2.time() < 10:
        #print timer2.time()
        for k in Rostopics.keys():
            timer.message(d2s(k,"=",P[k]))



