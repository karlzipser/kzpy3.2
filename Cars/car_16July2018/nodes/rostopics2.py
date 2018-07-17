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

Rostopics = [
    ('steer',Int),
    ('motor',Int),
    ('cmd/steer',Int),
    ('cmd/motor',Int),
    ('network_servo_percent',Int),
    ('network_motor_percent',Int),   
    ('human_agent',Int),
    ('behavioral_mode',Str),
    ('button_number',Int), 
    ('encoder',Float),
    ('gyro',Vec3),
    ('gyro_heading',Vec3),
    ('acc',Vec3)
    ]

callback_strs = []
subscriber_strs = []
P_strs = ['P = {}']
for topic in Rostopics:
    name = B+topic[0]
    callback_name = 'callback_'+get_safe_name(name)
    if topic[1] == Vec3:
        callback_strs.append(d2n("def ",callback_name,"(msg):","\n\tP['",name,"'] = (msg.x,msg.y,msg.z)\n"))
    else:
        callback_strs.append(d2n("def ",callback_name,"(msg):","\n\tP['",name,"'] = msg.data\n"))
    subscriber_strs.append(d2n("rospy.Subscriber('",name,"', ",topic[1],", callback=",callback_name,')\n'))
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
    P['PAUSE'] = False
    timer = Timer(0.01)

    """
    def printer_thread():
        while not P['ABORT']:
            time.sleep(0.01)
            if P['PAUSE']:
                continue
            for k in Rostopics.keys():
                t = k.replace('/bair_car/','')
                pd2s(t,"=\t",dp2(P[k],1))
    """

    import curses
    def pbar(window):
        while True:
            ctr = 0
            window.clear()
            for k in sorted(Rostopics.keys()):
                t = k.replace('/bair_car/','')
                window.addstr(ctr, 0, d2s(t,"=\t",P[k]))
                ctr += 1
                window.refresh()
            time.sleep(0.1)
    curses.wrapper(pbar)
"""
    import threading
    threading.Thread(target=printer_thread,args=[]).start()

    timer2 = Timer(60)
    q = '_'
    while q not in ['q','Q']:
        if timer2.check():
            break
        q = raw_input('')
        if q == ' ' and P['PAUSE']:
            P['PAUSE'] = False
        else:
            P['PAUSE'] = True
        time.sleep(0.1)
    P['ABORT'] = True
    print 'done.'
"""


