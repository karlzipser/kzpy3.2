#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)

runs = lo(opjD('Data/Network_Predictions/runs.pkl'))

u = []
for r in runs:
	u.append(pname(pname(r)))
u = list(set(u))

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

	sys_str = d2s(
					'python kzpy3/Data_app/make_shuffled_h5py_data.py',
					'src',
					'Data/1_TB_Samsung_n1/left_direct_stop__31Oct_to_1Nov2018/locations/local/left_direct_stop',
					'dst',
					'~/Desktop/Data/shuffled_h5py_data',
				)
	cg(sys_str)
	os.system(sys_str)
	os.system('rm '+in_progress)
