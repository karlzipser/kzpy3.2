from kzpy3.utils2 import *

USE_CURSES = False

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
    ('drive_mode',Int),
    ('encoder',Float),
    ('gyro',Vec3),
    ('gyro_heading',Vec3),
    ('acc',Vec3),
    ('Hz_acc',Float),
    ('Hz_mse',Float),
    ('Hz_network',Float)
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




def get_bag_info():

    try:

        latest_rosbag_folder = most_recent_file_in_folder(opj('/media',username,'rosbags'))

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

    bag_timer = Timer(5)

    if USE_CURSES:
        import curses
        def pbar(window):
            while True:

                ctr = 0
                window.clear()
                for topic in Rostopics:
                    window.addstr(ctr, 0, d2s(topic[0],"=\t",P[B+topic[0]]))
                    ctr += 1
                    window.refresh()
                time.sleep(0.1)
        curses.wrapper(pbar)
    else:
        bag_str = ''
        while True:
            ctr = 0
            time.sleep(0.1)
            print(chr(27) + "[2J")
            for topic in Rostopics:
                val = P[B+topic[0]]
                if is_number(val),
                    val = dp(val,2)
                pd2s(topic[0],"=\t",val)
                ctr += 1
                if bag_timer.check():
                    bag_str = get_bag_info()
                    bag_timer.reset()
            print bag_str
            


