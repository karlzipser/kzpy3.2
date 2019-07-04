from kzpy3.vis3 import *
import Menu.main
import kzpy3.drafts.Grapher.main as main

Q = Menu.main.start_Dic(
    dic_project_path=opjk('drafts/Grapher'),
    Dics={},
    Arguments={
        'menu':False,
        'read_only':False,
    }
)
T = Q['Q']

# cd /media/nvidia/rosbags/processed_20Jun19_15h14m12s/tegra-ubuntu_13Mar19_17h52m59s

import kzpy3.drafts.Grapher.defaults as defaults
P = defaults.P


if HAVE_ROS:
    import rospy
    import std_msgs.msg
    import geometry_msgs.msg
    ###################################################################
    #
    rospy.init_node('control_node',anonymous=True,disable_signals=True)
    #
    ###################################################################
    C = {}
    C['encoder'] = 0.
    C['encoder_time'] = time.time()
    bcs = '/bair_car'
    s = 0.9
    def encoder_callback(msg):

        C['encoder'] = msg.data
        C['encoder_time'] = time.time()
    rospy.Subscriber(bcs+'/encoder', std_msgs.msg.Float32, callback=encoder_callback)


if __name__ == '__main__':
    
    threading.Thread(target=main.grapher,args=[]).start()
    prnt = Timer(1)
    show_timer = Timer(T['times']['show'])
    
    while True:
        T = Q['Q']
        time.sleep(T['params']['thread_delay'])


        if HAVE_ROS:
            T['data']['a']['value'] = C['encoder']
        else:
            T['data']['a']['value'] = np.sin(5*time.time())
        T['data']['b']['value'] = np.sin(2*time.time())
        T['data']['c']['value'] = np.sin(20*time.time())
        #prnt.message(d2s(T['read_only']['ABORT']))
        if show_timer.check():
            show_timer.reset()
            k = mci(P['images']['big'],delay=1,scale=1)
            if k == ord('q'):
                CA()
                #T['read_only']['ABORT'] = True
                T['params']['ABORT'] = True
                break
        if T['params']['ABORT']:
            break
    cb('main() done.')


#EOF