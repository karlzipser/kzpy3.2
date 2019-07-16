#!/usr/bin/env python
from kzpy3.utils3 import *
assert HAVE_ROS

current_bag_number = 0

def get_bag_info():
	global current_bag_number
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
	print current_bag_number
	answer = get_bag_info()
	print answer
	s1 = d2s('rm',opjD('bw.txt'))
	s2 = d2s('rostopic bw /bair_car/zed/left/image_rect_color >',opjD('bw.txt'))
	s3 = 'killall rostopic'
	print s1
	print s2
	print s3
	unix(s1);raw_enter()
	unix(s2);raw_enter()
	unix(s3);raw_enter()
	time.sleep(1)