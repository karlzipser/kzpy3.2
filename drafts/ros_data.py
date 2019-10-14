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


if __name__ == '__main__':
	runs_with_lidar = []
	top = opjD('Data')
	#top = opjm('rosbags')
	M = find_files_recursively(top,'original_*',FILES_ONLY=True)
	src = M['src']
	for k in M['paths'].keys():
		p = opj(src,k,M['paths'][k][0])
		r = k.split('/')[-1]
		answer = h5py_file_has_topic(p,'image')
		print r,answer
		if answer:
			runs_with_lidar.append(r)
	soD(runs_with_lidar,'runs_with_lidar')