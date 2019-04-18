#!/usr/bin/env python
from kzpy3.utils3 import *
import rospy
import std_msgs.msg
import default_values
exec(identify_file_str)

try:
    temp_file = opjm('rosbags/__temp__')
    unix('touch '+temp_file)
    os.remove(temp_file)
except:
    while not rospy.is_shutdown():
        cr('*** not saving data ***',time_str())
        time.sleep(30)

for n in ['new','active']:
    os.system(d2s("mkdir -p",opjm('rosbags',n)))

foldername_prefix = os.environ["COMPUTER_NAME"]

foldername = d2n(foldername_prefix,'_',time_str())
time.sleep(3)


if __name__ == '__main__':
    rospy.init_node('rosbag_node',anonymous=True,disable_signals=True)
    save_pub = rospy.Publisher('data_saving', std_msgs.msg.Int32, queue_size=100)
    fl = gg(opjm('rosbags/active/*.active'))

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
                f_rec = os.path.join(bag_rec_folder, f)
                f_mv = os.path.join(bag_mv_folder, f)
                start = time.time()
                subprocess.call(['mv', f_rec, f_mv])
                elapsed = time.time() - start
                if len(sggo(bag_rec_folder,'*.bag')) > 0:
                    unix('rm '+opj(bag_rec_folder,'*.bag')) # 27 Nov 2016, to remove untransferred bags
                save_pub.publish(std_msgs.msg.Int32(0))
            rate.sleep()
    except Exception as e:
        print("********** Exception ***********************")
        default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)

    default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)

