from kzpy3.vis3 import *



def has_subdirectory(path):
	assert os.path.isdir(path) == True
	in_dir = sggo(path,'*')
	for f in in_dir:
		if os.path.isdir(f):
			return True
	return False



def all_files_have_suffix(path,suffix):
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
	if all_files_have_suffix(path,'bag'):
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
	
	if fname(path)[0] == '_':
		cs("ignorning",path,"because of leading '_'")
		return

	if fname(path) == 'active':
		cs("ignorning",path,"because of leading 'active'")
		return

	if os.path.isdir(path) == False:
		CS(path,exception=True)
		assert False

	in_dir = sggo(path,'*')

	for f in in_dir:
		if os.path.isdir(f):
			classify_data(opj(path,f),R)

	run_name = fname(path)

	if run_name not in ['lost+found']:

		spath = path.replace(opjm(),'')

		if is_raw_run(path):
			if run_name not in R:
				R[run_name] = {}
			if 'raw' not in R[run_name]:
				R[run_name]['raw'] = {}
			if 'pre' not in R[run_name]:
				R[run_name]['pre'] = {}
			bag_paths = sggo(path,'*.bag')
			R[run_name]['raw'][spath] = []
			for b in bag_paths:
				R[run_name]['raw'][spath].append(fname(b))

		elif is_preprocessed_run(path):
			if run_name not in R:
				R[run_name] = {}
			if 'pre' not in R[run_name]:
				R[run_name]['pre'] = {}
			if 'raw' not in R[run_name]:
				R[run_name]['raw'] = {}
			h5py_paths = sggo(path,'*.h5py')
			R[run_name]['pre'][spath] = []
			for b in h5py_paths:
				R[run_name]['pre'][spath].append(fname(b))

	


def is_run_backed_up(run_name,backup_disks,raw_or_pre,R,print_success=False):
	
	raw_or_pre_str = '('+raw_or_pre+')'

	if run_name not in R:
		CS(d2s("1)",run_name,raw_or_pre_str,'is NOT backed up on',backup_disks),emphasis=True)
		return False

	backed_up = []
	
	for b in backup_disks:
		if len(sggo(opjm(b),'*')) == 0:
			CS("2) Error,",b,"is empty or not available.",exception=True)
			assert False
		for a in R[run_name][raw_or_pre]:
			v = a.split('/')[0]

			if b == v:
				backed_up.append(b)
		if b not in backed_up:
			CS(d2s("3)",run_name,raw_or_pre_str,'is NOT backed up on',b),emphasis=True)
		elif print_success:
			cs("4)",run_name,raw_or_pre,'is backed up on',b)
		#print a,v,b,backed_up
	for b in backup_disks:
		if b not in backed_up:
			return False
	return True




def is_disk_backed_up(
	disk_name,
	backup_disks,
	R=None,
	D=None,
	raw_or_pre=None,
	transfer_data_to_backup_disks=False
	):

	successes,failures = 0,0
	if D == None:
		D = {}
		classify_data(opjm(disk_name),D)
	if R == None:
		R = {}
		for b in backup_disks:
			classify_data(opjm(b),R)

	if raw_or_pre == None:
		raw_pre_lst = ['raw','pre']
	elif raw_or_pre == 'raw':
		raw_pre_lst = ['raw']
	elif raw_or_pre == 'pre':
		raw_pre_lst = ['pre']
	else:
		assert False

	for rp in raw_pre_lst:

		for run_name in D:
			
			if 'backed up' not in D[run_name]:
				D[run_name]['backed up'] = {}

			D[run_name]['backed up'][rp] = is_run_backed_up(run_name,backup_disks,rp,R)
				
			if D[run_name]['backed up'][rp]:
				successes += 1
			
			else:
				if rp in D[run_name]:
					if rp == 'raw':
						color = 'green'
					elif rp == 'pre':
						color = 'cyan'
					#print len( D[run_name][rp].keys()),rp
					if len( D[run_name][rp].keys()) > 0:
						run_path = D[run_name][rp].keys()[0]
						cs('can save',run_path,'to',backup_disks)
						if transfer_data_to_backup_disks:
							for b in backup_disks:
								dst_path = opjm(b,run_path)
								mkdir = d2s('mkdir -p',dst_path)
								cprint(mkdir,color)
								os.system(mkdir)
								cp = d2s("cp -r",opjm(run_path),pname(dst_path))
								cprint(cp+'\n',color)
								os.system(cp)


				failures += 1
	cs("successes:",successes,"failures:",failures)
	return D,R



def parens(n):
	return d2n('(',n,')')



tb = "  "

def print_data(R):
	print('\n')
	runs = sorted(R.keys())
	for r in runs:
		cprint(d2s(" run:",r),attrs=['bold'],color='yellow',on_color='on_blue')
		colors = {'pre':'yellow','raw':'blue'}
		for t in ['pre','raw']:
			#cprint(d2s(tb,t))
			pr_runs = sorted(R[r][t])
			#print type(pr_runs),len(pr_runs)
			cprint(d2s(tb,t+':',parens(len(pr_runs))),colors[t])
			for u in pr_runs:
				cprint(d2s(tb,tb,u,parens(len(R[r][t][u]))),colors[t])

#EOF
		





