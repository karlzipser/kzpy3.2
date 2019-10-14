from kzpy3.utils3 import *

def bagfile_has_topic(bagfile,topic):
	ouput_txt = subprocess.check_output([
			'rosbag',
			'info',
			bagfile,
		])

	return topic in ouput_txt