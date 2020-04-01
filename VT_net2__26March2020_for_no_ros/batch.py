from kzpy3.utils3 import *

if Arguments['sys'] == 'main':
	sys_str = "python kzpy3/VT_net2__26March2020_for_no_ros/main.py --run_name "
elif Arguments['sys'] == 'h5py_write':
	sys_str = "python kzpy3/VT_net2__26March2020_for_no_ros/h5py_write.py --run_name "
else:
	assert False


run_lst = sggo(opjD('Data','Network_Predictions','*.net_predictions.pkl'))

for r in run_lst:
	run_name = fname(r).split('.')[0]
	cg(run_name)
	os.system(
		sys_str + run_name
	)