from kzpy3.vis3 import *
assert HAVE_ROS
import Menu.main
import kzpy3.drafts.Grapher.main as main
import kzpy3.drafts.Grapher.defaults as defaults
#import main
#import defaults
import kzpy3.drafts.Grapher.subscribe as subscribe
S = subscribe.S
#import rospy
#import std_msgs.msg
#import geometry_msgs.msg

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

###################################################################
#
subscribe.rospy.init_node('control_node',anonymous=True,disable_signals=True)
#
###################################################################

threading.Thread(target=main.grapher,args=[]).start()
prnt = Timer(1)
show_timer = Timer(T['times']['show'])
k = -1

while True:

    time.sleep(T['times']['thread_delay'])

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

    for topic in T['image_topics']:
        T['images'][topic]['value'] = S[topic]

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
        if k == ord(' '):
            T['pAUSE'] = not T['pAUSE']
            cg('pAUSE =',T['pAUSE'])
    if T['ABORT']:
        break

cb('main() done.')

#EOF
