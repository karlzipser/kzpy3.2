#!/usr/bin/env python
from kzpy3.utils3 import *
import default_values
exec(identify_file_str)

runs = lo(opjD('Data/Network_Predictions/runs.pkl'))
cb(runs)

for r in runs:
	working_runs = sggo(default_values._['dst path'],'*')
	cg(working_runs)
	#cr('working_runs',working_runs)
	cg('run =',r)
	break_continue = False
	for w in working_runs:
		#cy(1,w,2,r)
		if fname(r) in w:
			#cr('********** fname(r) in w **********')
			break_continue = True
			break
	#raw_enter()
	if break_continue:
		continue
	sys_str = 'mkdir -p ' + opj(default_values._['dst path'])
	cr(sys_str)
	os.system(sys_str)
	in_progress = opj(default_values._['dst path'],fname(r)+'.in_progress')
	sys_str = "touch "+in_progress
	cr(sys_str)
	os.system(sys_str)
	sys_str = "python kzpy3/VT_net2_/main.py run "+fname(r)
	cr(sys_str)
	os.system(sys_str)
	os.system('rm '+in_progress)
