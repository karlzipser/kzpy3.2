from kzpy3.utils3 import *

run_lst = sggo(opjD('Data','Network_Predictions','*.net_predictions.pkl'))

for r in run_lst:
	run_name = fname(r).split('.')[0]
	cg(run_name)
	os.system(
		"python kzpy3/VT_net2__26March2020_for_no_ros/main.py --run_name " + run_name
	)