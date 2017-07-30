###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Car_Data_app'])
#
###############################
from Parameters_Module import *
import Data_Module
exec(identify_file_str)

_ = dictionary_access

for a in Args.keys():
    _(P,a,equals,_(Args,a)) #P[a] = Args[a]


"""
def Timeseries_Data(*args):
	Args = args_to_dictionary(args)
	D = {}
	D[ts],D[vals] = get_key_sorted_elements_of_dic(Args[tdic])
	D[topic] = Args[topic]
	D[meo+vals]
	True
	meo_paramv = _(P,MEO_PARAMS,_(D,topic)):
	if len(shape(D[vals])) == 2:
		for qv in range(shape(D[vals])[1]):

	return D
"""

def Timeseries_Data(*args):
	Args = args_to_dictionary(args)
	D = {}
	D[ts],D[vals] = get_key_sorted_elements_of_dic(Args[tdic])
	D[vals] = np.array(D[vals])
	True
	return D



if da(P,EXAMPLE1):
	dataset_pathv = 'ExtraDrive2/bdd_car_data_July2017_LCR'
	run_namev = 'direct_home_LCR_25Jul17_19h37m22s_Mr_Yellow'
	Preprocessed_data = lo(opjm(dataset_pathv,'meta',run_namev,'preprocessed_data.pkl'))
	#left_image_timestamps = 
	Original_timestamp_data = {}
	for kv in Preprocessed_data.keys():
		Original_timestamp_data[kv] = Timeseries_Data(topic,kv, tdic,Preprocessed_data[kv])
		print kv,len(Preprocessed_data[kv])
	for kv in Original_timestamp_data.keys():
		if len(shape(Original_timestamp_data[kv][vals])) == 2:
			if shape(Original_timestamp_data[kv][vals])[1] == 3:
				ctrv = 0
				for qv in [x,y,z]:
					new_keyv = kv+'_'+qv
					Original_timestamp_data[new_keyv] = {}
					Original_timestamp_data[new_keyv][ts] = Original_timestamp_data[kv][ts]
					Original_timestamp_data[new_keyv][vals] = Original_timestamp_data[kv][vals][:,ctrv]
					ctrv += 1
				del Original_timestamp_data[kv]
				
	Left_timestamp_data = {}
	Left_timestamp_data[ts] = Original_timestamp_data[left_image][ts]

	Left_timestamp_data[right_ts] = []
	for iv in range(len(Original_timestamp_data[left_image][vals])):
		Left_timestamp_data[right_ts].append(Original_timestamp_data[right_image][ts][iv])
	Left_timestamp_data[right_ts] = np.array(Left_timestamp_data[right_ts])
	assert( np.abs( 0.03 - np.median(Left_timestamp_data[ts] - Left_timestamp_data[right_ts]) ) < 0.01 )

	for kv in Original_timestamp_data.keys():
		if kv != left_image and kv != right_image:
			if len(Original_timestamp_data[kv][ts]) > 0:
				Left_timestamp_data[kv] = np.interp(Left_timestamp_data[ts],
					Original_timestamp_data[kv][ts],Original_timestamp_data[kv][vals])

	"""

	assert left-right image timestamp correspondence
	get meo for acc xyz, encoder, gyroheading xyz
	get imu std



	xv,yv = get_key_sorted_elements_of_dic(ov[left_image])
	xv = np.array(xv)
	yv = np.array(yv)
	#yv=yv[:,1]
	#ymv = np.array(meo(yv,200))




	if False:
		vv = []
		for iv in range(100,81000):
			vv.append(np.std(yv[iv-50:iv+50]))
		plot(vv)
	"""
#EOF