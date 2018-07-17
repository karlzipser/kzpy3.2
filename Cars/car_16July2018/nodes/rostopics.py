from kzpy3.utils2 import *

"""
Rostopics = {'/bair_car/steer':{'type':Int},
    '/bair_car/motor':{'type':Int},
    '/bair_car/encoder':{'type':Float}
    }
"""

Int = 'std_msgs.msg.Int32'
Float = 'std_msgs.msg.Float32'
Vec3 = 'geometry_msgs.msg.Vector3'
Str = 'std_msgs.msg.String'
B = '/bair_car/'

Rostopics = {B+'cmd/steer':{'type':Int},
    B+'cmd/motor':{'type':Int},
    B+'human_agent':{'type':Int},
    B+'behavioral_mode':{'type':Str},
    B+'button_number':{'type':Int}, 
    B+'steer':{'type':Int},
    B+'motor':{'type':Int},
    B+'network_servo_percent':{'type':Int},
    B+'network_motor_percent':{'type':Int},
    B+'encoder':{'type':Float},
    B+'gyro':{'type':Vec3},
    B+'gyro_heading':{'type':Vec3},
    B+'acc':{'type':Vec3}
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

    P['ABORT'] = False
    timer = Timer(0.001)
    def printer_thread():
        while not P['ABORT']:
        for k in Rostopics.keys():
            t = k.replace('/bair_car','')
            timer.message(d2s(t,"=\t",P[k]))
    threading.Thread(target=printer_thread,args=[]).start()

    q = '_'
    while q not in ['q','Q']:
        q = raw_input('')
        if Parameters['ABORT']:
            break
        time.sleep(0.1)
    Parameters['ABORT'] = True
    print 'done.'



