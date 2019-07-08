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

        s = T['data']['slow_encoder']['s']
        if T['data']['slow_encoder']['value'] == None:
            T['data']['slow_encoder']['value'] = 0.

        if T['data']['encoder']['value'] == None:
            T['data']['encoder']['value'] = 0.
        T['data']['slow_encoder']['value'] = \
            s*T['data']['slow_encoder']['value'] + (1-s)*T['data']['encoder']['value']


        for topic in T['topics']:
            if topic in S:
                T['data'][topic]['value'] = S[topic]
                print topic,S[topic]
                #if 's' in topics:

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
