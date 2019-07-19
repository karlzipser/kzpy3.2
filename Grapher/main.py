from kzpy3.vis3 import *
import Menu.main
import kzpy3.Grapher.grapher as grapher
import kzpy3.Grapher.defaults as defaults
import kzpy3.drafts.Markov.main as Markov_main

Q = Menu.main.start_Dic(
    dic_project_path=opjk('Grapher'),
    Dics={},
    Arguments={
        'menu':False,
        'read_only':False,
    }
)
T = Q['Q']
Q['load']()

P = defaults.P
P['still'] = {}
P['still']['end'] = False
P['still']['begin'] = False
P['direction'] = 0
P['just_stopped_from_forward_timer'] = Timer(1/3.)
P['box_prev'] = 'still'
P['box'] = 'still'

if HAVE_ROS:
    import kzpy3.Grapher.subscribe as subscribe
    import std_msgs.msg
    S = subscribe.S
    Pub = {}
    Pub['drive_direction'] = rospy.Publisher('drive_direction',std_msgs.msg.Int32,queue_size=1)
    Pub['just_stopped_from_forward'] = rospy.Publisher('just_stopped_from_forward',std_msgs.msg.Int32,queue_size=1)
    pub_timer = Timer(1/30.)
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
        if topic.replace('_var','') in S:
            if '_var' in topic:
                T['data'][topic]['value'] = np.var(S[topic])
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



Directions = {
    'still': 0,
    'slow_forward': 1,
    'fast_forward': 1,
    'slow_backward': -1,
    'fast_backward': -1,
}

grab_xy_point_timer = Timer(1/10.)
xy_plot_timer = Timer(5)
save_xy_point_timer = Timer(30)
xy_points = []
Xy_bins = {}

while True:

    time.sleep(T['times']['thread_delay'])

    Q['load']()

    if HAVE_ROS:

        #print S['button_number']
        if S['button_number'] == 4:
            T['parameters']['the_motor'] = 'human/motor'
        else:
            T['parameters']['the_motor'] = 'cmd/motor'
            
        if T['parameters']['grab_xy_points']:
            if grab_xy_point_timer.check():
                grab_xy_point_timer.reset()
                x = T['data'][T['parameters']['the_motor']]['value']
                y = T['data']['encoder']['value']
                if is_number(x) and is_number(y):
                    if x < 49:
                        y *= -1
                    xy_points.append([x,y])
                    ix = intr(x)
                    if ix not in Xy_bins:
                        Xy_bins[ix] = []
                    Xy_bins[ix].append(y)

            if T['parameters']['plot_xy_points']:
                if xy_plot_timer.check():
                    xy_plot_timer.reset()
                    medians = []
                    xbins = []
                    for x in sorted(Xy_bins.keys()):
                        medians.append(np.median(Xy_bins[x]))
                        xbins.append(x)
                    figure('xy')
                    clf()
                    #pts_plot(xy_points)
                    plot(xbins,medians,'k.-')
                    spause()

            if T['parameters']['save_xy_points']:
                if save_xy_point_timer.check():
                    save_xy_point_timer.reset()
                    cy('save xy_points')
                    so(opjm('rosbags/xy_points'),xy_points)

        #S['encdoer_list']
        #print S['button_number'],T['parameters']['the_motor'],S['human/motor'],S['cmd/motor']


        assign_values_and_smoothed_values(T)

        if T['data']['encoder']['value'] != None and \
            T['data'][T['parameters']['the_motor']]['value'] != None:
            P['box_prev'] = P['box']
            P['box'] = Markov_main.Driving_direction_model['step'](
                {
                    'encoder': T['data']['encoder']['value'],
                    'motor': T['data'][T['parameters']['the_motor']]['value'],            
                }
            )
        if P['box_prev'] in ['slow_forward','fast_forward'] and P['box'] == 'still':
            P['just_stopped_from_forward_timer'].reset()
        else:
            pass #cr('no data for markov')



        if pub_timer.check():
            pub_timer.reset()
            print P['box']
            Pub['drive_direction'].publish(data=Directions[P['box']])

            if not P['just_stopped_from_forward_timer'].check():
                Pub['just_stopped_from_forward'].publish(data=1)
            else:
                Pub['just_stopped_from_forward'].publish(data=0)




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
