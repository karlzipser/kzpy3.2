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


if HAVE_ROS:
    import kzpy3.drafts.Grapher.subscribe as subscribe
    S = subscribe.S
    ###################################################################
    #
    subscribe.rospy.init_node('control_node',anonymous=True,disable_signals=True)
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

        d = 0
        if T['data']['encoder']['value_smooth'] > 0.1:
            if T['data']['cmd/motor']['value_smooth'] > 50:
                d = 1
            elif T['data']['cmd/motor']['value_smooth'] < 48:
                d = -1
        T['data']['drive_direction']['value'] = d


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
