from kzpy3.vis3 import *
import Menu.main
import kzpy3.drafts.Grapher.grapher as grapher
import kzpy3.drafts.Grapher.defaults as defaults

Q = Menu.main.start_Dic(
    dic_project_path=opjk('drafts/Grapher'),
    Dics={},
    Arguments={
        'menu':False,
        'read_only':False,
    }
)
T = Q['Q']

P = defaults.P

still_stop = False
still_start = False
the_motor = 'human/motor'

if HAVE_ROS:
    import kzpy3.drafts.Grapher.subscribe as subscribe
    import std_msgs.msg
    S = subscribe.S
    Pub = {}
    Pub['drive_direction'] = rospy.Publisher('drive_direction',std_msgs.msg.Int32,queue_size=1)
    pub_timer = Timer(0.1)
    ###################################################################
    #
    subscribe.rospy.init_node('grapher_node',anonymous=True,disable_signals=True)
    #
    ###################################################################


threading.Thread(target=grapher.grapher,args=[]).start()
prnt = Timer(1)
show_timer = Timer(T['times']['show'])
k = -1
ignore_repeat = Timer(0.2)


while True:

    time.sleep(T['times']['thread_delay'])

    if HAVE_ROS:

        for topic in T['topics']:
            if topic in S:
                T['data'][topic]['value'] = S[topic]
                if 's' in T['data'][topic]:
                    s = T['data'][topic]['s']
                    if 'value_smooth' not in T['data'][topic]:
                       T['data'][topic]['value_smooth'] = T['data'][topic]['value'] 
                    T['data'][topic]['value_smooth'] = \
                        s*T['data'][topic]['value_smooth'] + (1-s)*T['data'][topic]['value']


        if T['data']['encoder']['value_smooth'] < T['parameters']['still_threshold']:
            still_stop = False
            if still_start == False:
                still_start = Timer()
            q = 1
        else:
            still_start = False
            if still_stop == False:
                still_stop = Timer()
            q = 0

        if still_start != False:
            t0 = still_start.time()
        else:
            t0 = 0

        if still_stop != False:
            t1 = still_stop.time()
        else:
            t1 = 0

        ##cg(dp(t0),still_start,dp(t1),still_stop)

        if q == 1:
            d = 0
        elif T['data']['encoder']['value_smooth'] > T['parameters']['not_still_threshold']:
            if still_start != False:
                if still_start.time() > 0.2:
                    if T['data'][the_motor]['value_smooth'] > 50:
                        d = 1
                    elif T['data'][the_motor]['value_smooth'] < 48:
                        d = -1
            elif still_stop != False:
                if still_stop.time() > 0.2:
                    if T['data'][the_motor]['value_smooth'] > 50:
                        d = 1
                    elif T['data'][the_motor]['value_smooth'] < 48:
                        d = -1

        T['data']['drive_direction']['value'] = d
        if pub_timer.check():
            pub_timer.reset()
            Pub['drive_direction'].publish(data=d)

        T['data']['still']['value'] = q




        for topic in T['image_topics']:
            T['images'][topic]['value'] = S[topic]

    else:
        T['data']['a']['value'] = np.sin(5*time.time())
        T['data']['b']['value'] = np.sin(2*time.time())
        T['data']['c']['value'] = np.sin(10*time.time())


    if show_timer.check():
        if k == ord('c'):
            T['CLEAR'] = True
        if T['CLEAR']:
            T['CLEAR'] = False
            P['images']['big'] *= 0
        show_timer.reset()
        k = mci(P['images']['big'],delay=1,scale=1)
        if k == ord('q'):
            CA()
            T['ABORT'] = True
            break
        if k == ord(' ') and ignore_repeat.check():
            ignore_repeat.reset()
            T['pAUSE'] = not T['pAUSE']
            cg('pAUSE =',T['pAUSE'])
    if T['ABORT']:
        break

cb('main() done.')

#EOF
