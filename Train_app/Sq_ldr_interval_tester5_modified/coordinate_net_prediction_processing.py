#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)

runs = lo(opjD('Data/Network_Predictions/runs.pkl'))

for r in runs:
	sys_str = "python kzpy3/Cars/n11Dec2018/nodes/network_node__for_playback.py "+ \
		"graphics 0 dst_folder /home/karlzipser/Desktop/Data/Network_Predictions run_folder "+r
	cg(sys_str)
	os.system(sys_str)
