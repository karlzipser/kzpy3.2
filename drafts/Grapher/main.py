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
P['still'] = {}
P['still']['end'] = False
P['still']['begin'] = False
P['direction'] = 0

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


# put rate dependence of s into equation.

def assign_values_and_smoothed_values(T):
    for topic in T['topics']:
        if topic.replace('_list','') in S:
            if '_list' in topic:
                T['data'][topic]['value'] = max(S[topic])
                #cb(topic,T['data'][topic]['value'])
            else:
                T['data'][topic]['value'] = S[topic]
            #cr(S[topic])
            if 's' in T['data'][topic]:
                s = T['data'][topic]['s']
                if 'value_smooth' not in T['data'][topic]:
                   T['data'][topic]['value_smooth'] = T['data'][topic]['value'] 
                T['data'][topic]['value_smooth'] = \
                    s*T['data'][topic]['value_smooth'] + (1-s)*T['data'][topic]['value']



def evaluate_if_is_car_still(T,P):
    if T['data']['encoder']['value_smooth'] < T['parameters']['still_threshold']:
        #P['still']['end'] = False
        if P['still']['begin'] == False:
            P['still']['begin'] = Timer()
        #P['still']['value'] = 1
    else:
        P['still']['begin'] = False
        if P['still']['end'] == False:
            P['still']['end'] = Timer()
        P['still']['value'] = 0
    T['data']['still']['value'] = P['still']



def determine_and_publish_direction(T,P):
    if 'value_smooth' in T['data'][T['parameters']['the_motor']]:
        if P['still']['value'] == 1:
            P['direction'] = 0
        elif T['data']['encoder']['value_smooth'] > T['parameters']['not_still_threshold']:
            if P['still']['begin'] != False:
                if P['still']['begin'].time() > 0.2:
                    if T['data'][T['parameters']['the_motor']]['value_smooth'] > 50:
                        P['direction'] = 1
                    elif T['data'][T['parameters']['the_motor']]['value_smooth'] < 48:
                        P['direction'] = -1
            elif P['still']['end'] != False:
                if P['still']['end'].time() > 0.2:
                    if T['data'][T['parameters']['the_motor']]['value_smooth'] > 50:
                        P['direction'] = 1
                    elif T['data'][T['parameters']['the_motor']]['value_smooth'] < 48:
                        P['direction'] = -1

        T['data']['drive_direction']['value'] = P['direction']

        if pub_timer.check():
            pub_timer.reset()
            Pub['drive_direction'].publish(data=P['direction'])





while True:

    time.sleep(T['times']['thread_delay'])

    if HAVE_ROS:


        #S['encdoer_list']



        assign_values_and_smoothed_values(T)

        #evaluate_if_is_car_still(T,P)

        #determine_and_publish_direction(T,P)

    





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
