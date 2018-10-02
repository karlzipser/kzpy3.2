from kzpy3.utils3 import *

current_bag_number = 0

def get_bag_info():
	print 'get_bag_info'
    try:
        latest_rosbag_folder = most_recent_file_in_folder(opjm('rosbags'))
        latest_rosbag = most_recent_file_in_folder(latest_rosbag_folder)
        bag_num = int(fname(latest_rosbag).split('_')[-1].split('.')[0])
        bag_size = os.path.getsize(latest_rosbag)
        bag_size = dp(bag_size/1000000000.)
        print latest_rosbag_folder,latest_rosbag,bag_num,bag_size,'current_bag_number=',current_bag_number
        if (bag_num == current_bag_number+1) and bag_size > 0.5:
        	current_bag_number += 1
        	return True
        else:
        	return False
    except:
        return False

while True:
	time.sleep(1)
	print get_bag_info()