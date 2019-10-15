from kzpy3.utils3 import *
from kzpy3.drafts.runs_with_points import *

src = Arguments['src']
dst = Arguments['dst']
os.system('mkdir -p '+dst)
#num_folders = Arguments['num_folders']

M = find_files_recursively(src,'*.bag',FILES_ONLY=True)

for k in M['paths'].keys():
	run_name = k.split('/')[-1]
	if run_name in runs_with_points:
		#print run_name,opj(M['src'],k)
		os.system(d2s('ln -s',opj(M['src'],k),opj(dst,run_name)))
	else:
		pass
		#print run_name,False


"""
python kzpy3/drafts/setup_run_links.py --src /media/karlzipser/A3 --dst ~/Desktop/runs_with_points__links

Data src ~/Desktop/runs_with_points__links dst ~/Desktop/runs_with_points__h5py
"""

#EOF
