from kzpy3.utils3 import *

def bagfile_has_topic(bagfile,topic):
	ouput_txt = subprocess.check_output([
			'rosbag',
			'info',
			bagfile,
		])

	return topic in ouput_txt


def h5py_file_has_topic(h5py_file,topic):
	F = h5r(h5py_file)
	answer = topic in F.keys()
	F.close()
	return answer