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

if False:
    ###################################################################
    #
    S = {}
    S['encoder'] = 0.
    S['encoder_time'] = time.time()
    S['gyro_heading_x'] = 0
    S['gyro_heading_x_prev'] = 0
    S['ts_prev'] = 0
    S['ts'] = 0
    S['d_heading'] = 0

    bcs = '/bair_car'
    s = 0.9

    def encoder_callback(msg):
        S['encoder'] = msg.data
        S['encoder_time'] = time.time()
    rospy.Subscriber(bcs+'/encoder', std_msgs.msg.Float32, callback=encoder_callback)

    def gyro_heading_x_callback(data):
        S['gyro_heading_x_prev'] = S['gyro_heading_x']
        S['gyro_heading_x'] = data.x
        S['d_heading'] = 2*(S['gyro_heading_x']-S['gyro_heading_x_prev'])
        S['ts_prev'] = S['ts']
        S['ts'] = time.time()
        S['sample_frequency'] = 1.0 / (S['ts']-S['ts_prev'])
    rospy.Subscriber(bcs+'/gyro_heading', geometry_msgs.msg.Vector3, callback=gyro_heading_x_callback,queue_size=5)
    #
    ###################################################################




threading.Thread(target=main.grapher,args=[]).start()
prnt = Timer(1)
show_timer = Timer(T['times']['show'])

while True:

    time.sleep(T['times']['thread_delay'])

    for topic in T['topics']:
        T['data'][topic]['value'] = S[topic]

    for topic in T['image_topics']:
        T['images'][topic]['value'] = S[topic]

    if show_timer.check():
        if T['CLEAR']:
            T['CLEAR'] = False
            P['images']['big'] *= 0
        show_timer.reset()
        k = mci(P['images']['big'],delay=1,scale=1)
        if k == ord('q'):
            CA()
            T['ABORT'] = True
            break
    if T['ABORT']:
        break

cb('main() done.')


#EOF
