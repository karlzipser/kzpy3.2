from kzpy3.utils import *

data_path = opjD('bair_car_data')
meta_path = opj(data_path,'meta')
rgb_1to4_path = opj(data_path,'rgb_1to4')
run_full_names = gg(opj(meta_path,'*'))
run_full_names += gg(opj(rgb_1to4_path,'*'))
run_names = []
for r in run_full_names:
	run_names.append(fname(r))
print len(run_names)
run_names = sorted(list(set(run_names)))
print len(run_names)
"""
for r in run_names:
	run_meta_path = opj(meta_path,r)
	if len(gg(run_meta_path)) == 0:
		cprint(d2s(r,'not in meta'),'red')
	else:
		cprint(d2s(r,'in meta'),'yellow')
"""
for r in run_names:
	run_rgb_path = opj(rgb_1to4_path,r)
	if len(gg(run_rgb_path)) == 0:
		cprint(d2s(r,'not in rgb_1to4'),'red')
	else:
		cprint(d2s(r,'in rgb_1to4'),'yellow')
		files = gg(opj(run_rgb_path,'*.bag.pkl'))
		
		min_size = 10**9
		max_size = 0
		for f in files:
			fsize = os.path.getsize(f)
			if fsize < min_size:
				min_size = fsize
			if fsize > max_size:
				max_size = fsize
		cprint(d2s('\t',len(files),'files',(min_size/10**6,max_size/10**6)),'blue')

run_data = {}
