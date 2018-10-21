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

	if 'raw' not in R[run_name]:
		R[run_name]['raw'] = {}
	if 'pre' not in R[run_name]:
		R[run_name]['pre'] = {}

	if is_raw_run(path):
		if run_name not in R:
			R[run_name] = {}
		bag_paths = sggo(path,'*.bag')
		R[run_name]['raw'][spath] = []
		for b in bag_paths:
			R[run_name]['raw'][spath].append(fname(b))

	elif is_preprocessed_run(path):
		if run_name not in R:
			R[run_name] = {}
		h5py_paths = sggo(path,'*.h5py')
		R[run_name]['pre'][spath] = []
		for b in h5py_paths:
			R[run_name]['pre'][spath].append(fname(b))

	


def is_run_backed_up(run_name,backup_disks,raw_or_pre,R,print_success=False):
	if run_name not in R:
		CS(d2s(run_name,raw_or_pre_str,'is NOT backed up on',b),emphasis=True)
		return False
	backed_up = []
	raw_or_pre_str = '('+raw_or_pre+')'
	for b in backup_disks:
		for a in R[run_name][raw_or_pre]:
			v = a.split('/')[0]
			if b == v:
				backed_up.append(b)
		if b not in backed_up:
			CS(d2s(run_name,raw_or_pre_str,'is NOT backed up on',b),emphasis=True)
		elif print_success:
			cs(run_name,raw_or_pre,'is backed up on',b)
	if len(backed_up) == len(backup_disks):
		return True
	else:
		return False


def is_disk_backed_up(disk_name,backup_disks,R):
	D = classify_data(opjm(disk_name),R)
	for raw_or_pre in ['raw','pre']:
		for run_name in D:
			D[run_name]['backed up'] = is_run_backed_up(run_name,backup_disks,raw_or_pre,R)
	return D





#EOF
		





