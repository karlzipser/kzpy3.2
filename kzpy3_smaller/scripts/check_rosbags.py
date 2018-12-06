#!/usr/bin/python
from kzpy3.utils2 import *

while True:

	try:

		latest_rosbag_folder = most_recent_file_in_folder(opj('/media',username,'rosbags'))

		latest_rosbag = most_recent_file_in_folder(latest_rosbag_folder)

		bag_num = fname(latest_rosbag).split('_')[-1]

		bag_time = os.path.getmtime(latest_rosbag)

		bag_time = int( time.time() - bag_time)

		bag_size = os.path.getsize(latest_rosbag)

		bag_size = dp(bag_size/1000000000.)

		print(d2s(bag_num,bag_size,'GB',bag_time,'s',time_str('TimeShort')))

		time.sleep(5)

	except:

		print('rosbags not found or other problem')
		time.sleep(5)