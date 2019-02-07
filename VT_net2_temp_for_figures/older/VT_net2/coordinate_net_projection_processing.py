#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)

runs = lo(opjD('Data/Network_Predictions/runs.pkl'))


for r in runs:
	working_runs = sggo(opjD('Data/Network_Predictions_projected/*'))
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

	in_progress = opjD('Data/Network_Predictions_projected',fname(r)+'.in_progress')
	os.system("touch "+in_progress)
	sys_str = "python kzpy3/VT_net/main.py run "+fname(r)
	cg(sys_str)
	os.system(sys_str)
	os.system('rm '+in_progress)
