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


if False:#__name__ == '__main__':
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

	if False:
		from kzpy3.drafts.runs_with_points import *
		top = opjm('ExtraDrive3')
		M = find_files_recursively(top,'*.bag',FILES_ONLY=True)
		runs = M['parent_folders']
		for r in runs_with_points:
			if r in runs:
				print r


def find_h5py_runs_with_topic(topic,top,filetype):
	if filetype == 'h5py':
		pattern = 'original_*'
	elif filetype == 'bag':
		pattern = '*.bag'
	runs_with_topic = []
	M = find_files_recursively(top,pattern,FILES_ONLY=True)
	src = M['src']
	for k in M['paths'].keys():
		p = opj(src,k,M['paths'][k][0])
		r = k.split('/')[-1]
		if filetype == 'h5py':
			answer = h5py_file_has_topic(p,topic)
		elif filetype == 'bag':
			answer = bagfile_has_topic(p,topic)
		print r,answer
		if answer:
			runs_with_topic.append(k)
	soD(runs_with_topic,'runs_with_topic_'+topic)
	return runs_with_topic



def make_folder_of_links_to_runs_with_topic(folder_path,topic,top,filetype):
	os.system(d2s('mkdir -p',folder_path))
	runs_with_topic = find_h5py_runs_with_topic(topic,top,filetype)
	for r in runs_with_topic:
		run_name = fname(r)
		os.system(d2s('ln -s',opj(top,r),opj(folder_path,run_name)))


if False:
	make_folder_of_links_to_runs_with_topic(opjD('runs_with_image_topic'),'image',opjD(),'h5py')

