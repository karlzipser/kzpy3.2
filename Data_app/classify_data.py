from kzpy3.vis3 import *




def has_subdirectory(path):
	assert os.path.isdir(path) == True
	in_dir = sggo(path,'*')
	for f in in_dir:
		if os.path.isdir(f):
			return True
	return False


def all_files_with_suffix(path,suffix):
	in_dir = sggo(path,'*')
	ctr = 0
	for f in in_dir:
		if os.path.isfile(f):
			if f.split('.')[-1] != suffix:
				return False
			else:
				ctr += 1
	if ctr > 0:
		return True
	else:
		return False


def is_raw_run(path):
	if has_subdirectory(path):
		return False
	if all_files_with_suffix(path,'bag'):
		return True
	else:
		return False


def is_preprocessed_run(path):
	if has_subdirectory(path):
		return False
	if len(sggo(path,'*.bag')) > 0:
		return False
	F = sggo(path,'*.h5py')
	flip_images = False
	original_timestamp_data = False
	left_timestamp = False
	for f in F:
		if 'flip_images' in f:
			flip_images = True
		elif 'original_timestamp_data' in f:
			original_timestamp_data = True
		elif 'left_timestamp' in f:
			left_timestamp = True
	if flip_images and original_timestamp_data and left_timestamp:
		return True
	else:
		return False


def classify_data(path,R):
	cs(path)
	assert os.path.isdir(path) == True
	in_dir = sggo(path,'*')

	for f in in_dir:
		if os.path.isdir(f):
			classify_data(opj(path,f),R)

	run_name = fname(path)
	spath = path.replace(opjm(),'')

	if is_raw_run(path):
		if run_name not in R:
			R[run_name] = {}
		if 'raw' not in R[run_name]:
			R[run_name]['raw'] = {}
		bag_paths = sggo(path,'*.bag')
		
		R[run_name]['raw'][spath] = []
		for b in bag_paths:
			R[run_name]['raw'][spath].append(fname(b))

	elif is_preprocessed_run(path):
		if run_name not in R:
			R[run_name] = {}
		if 'pre' not in R[run_name]:
			R[run_name]['pre'] = {}
		h5py_paths = sggo(path,'*.h5py')
		R[run_name]['pre'][spath] = []
		for b in h5py_paths:
			R[run_name]['pre'][spath].append(fname(b))


def is_run_backed_up(run_name,backup_disks,R,raw_or_pre):
	for b in backup_disks:
		backed_up = False
		if a not in R:
			CS(d2s(run_name,raw_or_pre,'NOT backed up on',b),emphasis=True)
		for a in R[run_name][raw_or_pre]:
			v = a.split('/')[0]
			if b == v:
				backed_up = True
		if backed_up == False:
			CS(d2s(run_name,raw_or_pre,'NOT backed up on',b),emphasis=True)
			return False
		else:
			cs(run_name,raw_or_pre,'backed up on',b)
	return True





#EOF
		





