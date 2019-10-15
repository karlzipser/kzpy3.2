from kzpy3.utils3 import *
from kzpy3.drafts.runs_with_points import *

src = Arguments['src']
dst = Arguments['dst']
num_folders = Arguments['num_folders']

M = find_files_recursively(src,'*.bag',FILES_ONLY=True)

for k in M['paths'].keys():
	run_name = k.split('/')[-1]
	if run_name in runs_with_points:
		print run_name,k
	else:
		print run_name,False


