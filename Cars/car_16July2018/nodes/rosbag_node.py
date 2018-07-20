#!/usr/bin/env python
from kzpy3.utils2 import *
import os, sys, shutil, subprocess, time
import rospy
import std_msgs.msg

os.environ['STOP'] = 'False'

foldername_prefix = os.environ["COMPUTER_NAME"] #'run_'

spd2s()
foldername = d2n(foldername_prefix,'_',time_str())
time.sleep(3)

if __name__ == '__main__':
    rospy.init_node('rosbag_node', anonymous=True)
    save_pub = rospy.Publisher('data_saving', std_msgs.msg.Int32, queue_size=100)
    

    fl = gg(opjh('catkin_ws/src/bair_car/rosbags/*'))

    for f in fl:
         os.remove(f)

    assert(len(sys.argv) >= 3)

    bag_rec_folder = sys.argv[1] # '/home/ubuntu/catkin_ws/src/bair_car/rosbags'
    bag_mv_folder = sys.argv[2] # '/media/ubuntu/3131-3031/rosbags'
    bag_mv_folder = opj(bag_mv_folder,foldername)

    unix('mkdir '+bag_mv_folder)
    
    assert(os.path.exists(bag_rec_folder))
    assert(os.path.exists(bag_mv_folder))

    rate = rospy.Rate(2.0)

    try:
        while not rospy.is_shutdown():
            save_pub.publish(std_msgs.msg.Int32(0))
            for f in os.listdir(bag_rec_folder):
                if '.bag' != os.path.splitext(f)[1]:
                    continue
                save_pub.publish(std_msgs.msg.Int32(1) )
                print('Moving {0}'.format(f))
                f_rec = os.path.join(bag_rec_folder, f)
                f_mv = os.path.join(bag_mv_folder, f)
                # shutil.copy(f_rec, f_mv)
                start = time.time()
                subprocess.call(['mv', f_rec, f_mv])
                elapsed = time.time() - start
                unix('rm '+opj(bag_rec_folder,'*.bag')) # 27 Nov 2016, to remove untransferred bags
                print('Done in {0} secs\n'.format(elapsed))
                save_pub.publish(std_msgs.msg.Int32(0))
                
            rate.sleep()
    except Exception as e:
        print("********** Exception ***********************")
        print(e.message, e.args)
        print "rosbag_node.py Exception doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))"
        unix(opjh('kzpy3/scripts/kill_ros.sh'))
   print "rosbag_node.py end doing... unix(opjh('kzpy3/scripts/kill_ros.sh'))"
        unix(opjh('kzpy3/scripts/kill_ros.sh'))

