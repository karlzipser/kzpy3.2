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


# def Left_Timestamp_Data
if da(P,EXAMPLE1):
	dataset_pathv = 'ExtraDrive2/bdd_car_data_July2017_LCR'
	run_namev = 'direct_home_LCR_25Jul17_19h37m22s_Mr_Yellow'
	pathv = opjm(dataset_pathv,'meta',run_namev,'preprocessed_data.pkl')
	assert_disk_locations(pathv)
	Preprocessed_data = lo(opjm(dataset_pathv,'meta',run_namev,'preprocessed_data.pkl'))
	Original_timestamp_data = {}
	for kv in Preprocessed_data.keys():
		Original_timestamp_data[kv] = Timeseries_Data(topic,kv, tdic,Preprocessed_data[kv])
		print kv,len(Preprocessed_data[kv])
	for kv in Original_timestamp_data.keys():
		if len(shape(Original_timestamp_data[kv][vals])) == 2:
			if shape(Original_timestamp_data[kv][vals])[1] == 3:
				ctrv = 0
				for qv in [x]:#,y,z]:
					new_keyv = kv+'_'+qv
					Original_timestamp_data[new_keyv] = {}
					Original_timestamp_data[new_keyv][ts] = Original_timestamp_data[kv][ts]
					Original_timestamp_data[new_keyv][vals] = Original_timestamp_data[kv][vals][:,ctrv]
					ctrv += 1
				del Original_timestamp_data[kv]

	Left_timestamp_data = {}
	Left_timestamp_data[ts] = np.array(Original_timestamp_data[left_image][ts])

	Left_timestamp_data[right_ts] = []
	for iv in range(len(Original_timestamp_data[left_image][vals])):
		Left_timestamp_data[right_ts].append(Original_timestamp_data[right_image][ts][iv])
	Left_timestamp_data[right_ts] = np.array(Left_timestamp_data[right_ts])
	assert( np.abs( 0.03 - np.median(Left_timestamp_data[ts] - Left_timestamp_data[right_ts]) ) < 0.01 )

	for kv in sorted(Original_timestamp_data.keys()):
		if kv != left_image and kv != right_image:
			if len(Original_timestamp_data[kv][ts]) > 0:
				print('processing '+kv)
				Left_timestamp_data[kv] = np.interp(Left_timestamp_data[ts],
					Original_timestamp_data[kv][ts],Original_timestamp_data[kv][vals])
				if kv in P[MEO_PARAMS]:
					Left_timestamp_data[kv+'_meo'] = np.interp(Left_timestamp_data[ts],
						Original_timestamp_data[kv][ts],meo(Original_timestamp_data[kv][vals],P[MEO_PARAMS][kv]))

	Left_timestamp_data[state] = Left_timestamp_data[state].astype(int)

	Left_timestamp_data[left_ts_deltas] = 0.0 * Left_timestamp_data[ts]
	for iv in range(1,len(Left_timestamp_data[ts])):
		Left_timestamp_data[left_ts_deltas][iv] = Left_timestamp_data[ts][iv] - Left_timestamp_data[ts][iv-1]


	"""
	#get imu std

	if False:
		vv = []
		for iv in range(100,81000):
			vv.append(np.std(yv[iv-50:iv+50]))
		plot(vv)
	"""





#bag_folder_pathv = '/media/karlzipser/ExtraDrive4/Mr_Yellow_2June2017/processed/direct_rewrite_test_02Jun17_14h15m27s_Mr_Yellow'
#bag_folder_pathv = '/media/karlzipser/ExtraDrive4/Mr_Yellow_2June2017/processed/direct_rewrite_test_02Jun17_14h03m43s_Mr_Yellow'


def Original_Timestamp_Data(*args):
	Args = args_to_dictionary(args)
	D = {}
	bag_folder_pathv = Args[bag_folder_path]
	h5py_pathv = Args[h5py_path]
	True
	import rospy
	import rosbag
	import cv2
	import cv_bridge
	from cv_bridge import CvBridge, CvBridgeError
	bridge = cv_bridge.CvBridge()

	image_topicsv = ['zed/left/image_rect_color','zed/right/image_rect_color']
	single_value_topicsv = [steer,state,motor,encoder]
	vector3_topicsv = [acc,gyro,gps,gyro_heading]
	all_topicsv = image_topicsv + single_value_topicsv + vector3_topicsv
	bair_all_topicsv = []
	for v in all_topicsv:
		bair_all_topicsv.append('/bair_car/'+v)
	Rename = {}
	Rename['zed/left/image_rect_color'] = left_image
	Rename['zed/right/image_rect_color'] = right_image

	for topicv in all_topicsv:
		if 'zed' in topicv:
				topicv = Rename[topicv]
		D[topicv] = {}
		D[topicv][ts] = []
		D[topicv][vals] = []

	bag_filesv = sorted(glob.glob(opj(bag_folder_pathv,'*.bag')))
	
	cprint(d2s('Processing',len(bag_filesv),'bag files:'),'red')
	for bv in bag_filesv:
		cprint('\t'+bv,'blue')

	timerv = Timer(0)
	for bv in bag_filesv:
		timerv.reset()

		cprint(bv,'yellow')

		bagv = rosbag.Bag(bv)

		for mv in bagv.read_messages(topics=bair_all_topicsv):
			timestampv = round(mv[2].to_time(),3) # millisecond resolution
			assert(is_number(timestampv))
			topicv = mv[0].replace('/bair_car/','')
			if 'zed' in mv[0]:
				valv = bridge.imgmsg_to_cv2(mv[1],"rgb8")
				valv = cv2.resize(valv, (0,0), fx=0.25, fy=0.25)
			elif hasattr(mv[1], 'data'):
				if is_number(mv[1].data):
					valv = mv[1].data
			elif hasattr(mv[1], 'x'):
				valv = [mv[1].x,mv[1].y,mv[1].z]
				for nv in valv:
					assert(is_number(nv))
			elif hasattr(mv[1], 'latitude'):
				valv = [mv[1].latitude,mv[1].longitude,mv[1].altitude]
				for nv in valv:
					assert(is_number(nv))
			else:
				raise ValueError('ERROR because: topic '+topicv+' not processed.')
			if 'zed' in topicv:
				topicv = Rename[topicv]

			D[topicv][ts].append(timestampv)
			D[topicv][vals].append(valv)

		print(d2s('\t',dp(timerv.time()),'seconds'))

	D[topicv][ts] = np.array(D[topicv][ts])
	D[topicv][vals] = np.array(D[topicv][vals])

	run_namev = fname(bag_folder_pathv)
	
	unix('mkdir -p '+opj(h5py_pathv,run_namev))
	fv = h5py.File(opj(h5py_pathv,run_namev,'original_timestamp_data.h5py'),'w')
	for topicv in D.keys():
		print topicv
		groupv = fv.create_group(topicv)
		groupv.create_dataset(ts,data=D[topicv][ts])
		groupv.create_dataset(vals,data=D[topicv][vals])
	fv.close()
	return(D)


if da(P,EXAMPLE2):
	D = Original_Timestamp_Data(bag_folder_path,'/media/karlzipser/ExtraDrive4/Mr_Yellow_2June2017/processed/direct_rewrite_test_02Jun17_14h03m43s_Mr_Yellow',
		h5py_path,opjm('ExtraDrive2/bdd_car_data_July2017_LCR/h5py'))







#EOF


