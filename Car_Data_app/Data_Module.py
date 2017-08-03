from Parameters_Module import *
exec(identify_file_str)


def Original_Timestamp_Data(*args):
	"""
	Translate from .bag files to original_timestamp_data.h5py
	"""
	Args = args_to_dictionary(args)
	D = {}
	bag_folder_pathv = Args[bag_folder_path]
	h5py_pathv = Args[h5py_path]
	True
	run_namev = fname(bag_folder_pathv)
	unix('mkdir -p '+opj(h5py_pathv,run_namev))
	file_path = opj(h5py_pathv,run_namev,'original_timestamp_data.h5py')
	if os.path.exists(file_path):
		print(stars0v+file_path+' exists, doing nothing.'+stars1_)
		return None
	import rospy
	import rosbag
	import cv2
	import cv_bridge
	from cv_bridge import CvBridge, CvBridgeError
	bridge = cv_bridge.CvBridge()

	image_topicsv = ['zed/left/image_rect_color','zed/right/image_rect_color']
	single_value_topicsv = [steer,state,motor,encoder]
	vector3_topicsv = [acc,gyro,gps,gyro_heading]
	all_topics_ = image_topicsv + single_value_topicsv + vector3_topicsv
	bair_all_topics_ = []
	for v in all_topics_:
		bair_all_topics_.append('/bair_car/'+v)
	Rename = {}
	Rename['zed/left/image_rect_color'] = left_image
	Rename['zed/right/image_rect_color'] = right_image

	for topic_ in all_topics_:
		if 'zed' in topic_:
				topic_ = Rename[topic_]
		D[topic_] = {}
		D[topic_][ts] = []
		D[topic_][vals] = []

	bag_filesv = sorted(glob.glob(opj(bag_folder_pathv,'*.bag')))
	
	cprint(d2s('Processing',len(bag_filesv),'bag files:'),'red')
	for bv in bag_filesv:
		cprint('\t'+bv,'blue')

	timerv = Timer(0)

	#temp_counter = 0
	for bv in bag_filesv:
		#if temp_counter >= 2:
		#	break
		#temp_counter += 1
		timerv.reset()

		cprint(bv,'yellow')

		bagv = rosbag.Bag(bv)

		for m_ in bagv.read_messages(topics=bair_all_topics_):
			timestampv = round(m_[2].to_time(),3) # millisecond resolution
			assert(is_number(timestampv))
			topic_ = m_[0].replace('/bair_car/','')
			if 'zed' in m_[0]:
				valv = bridge.imgmsg_to_cv2(m_[1],"rgb8")
				valv = cv2.resize(valv, (0,0), fx=0.25, fy=0.25)
			elif hasattr(m_[1], 'data'):
				if is_number(m_[1].data):
					valv = m_[1].data
			elif hasattr(m_[1], 'x'):
				valv = [m_[1].x,m_[1].y,m_[1].z]
				for nv in valv:
					assert(is_number(nv))
			elif hasattr(m_[1], 'latitude'):
				valv = [m_[1].latitude,m_[1].longitude,m_[1].altitude]
				for nv in valv:
					assert(is_number(nv))
			else:
				raise ValueError('ERROR because: topic '+topic_+' not processed.')
			if 'zed' in topic_:
				topic_ = Rename[topic_]

			D[topic_][ts].append(timestampv)
			D[topic_][vals].append(valv)

		print(d2s('\t',dp(timerv.time()),'seconds'))

	D[topic_][ts] = np.array(D[topic_][ts])
	D[topic_][vals] = np.array(D[topic_][vals])

	for k_ in D.keys():
		if len(shape(D[k_][vals])) == 2:
			if shape(D[k_][vals])[1] == 3:
				D[k_][vals] = np.array(D[k_][vals])
				ctr_ = 0
				for q_ in [x,y,z]:
					new_key_ = k_+'_'+q_
					D[new_key_] = {}
					D[new_key_][ts] = D[k_][ts]
					D[new_key_][vals] = D[k_][vals][:,ctr_]
					ctr_ += 1
				del D[k_]

#	F = h5py.File(file_path,'w')
	F = h5w(file_path)
	for topic_ in D.keys():
		print topic_
		Group = F.create_group(topic_)
		Group.create_dataset(ts,data=D[topic_][ts])
		Group.create_dataset(vals,data=D[topic_][vals])
	F.close()
	return(D)



def _assign_right_image_timestamps(A):
	interp_dic = {}
	k,d = get_sorted_keys_and_data(A['right_image'])
	for i in range(0,len(k)-1):
		a = int(k[i]*1000)
		b = int(k[i+1]*1000)
		c = (a+b)/2
		for j in range(a,b):
			if j < c:
				v = k[i]
			else:
				v = k[i+1]
			interp_dic[j/1000.] = v
	return interp_dic

def _assign_right_image_timestamps2(F):
	interp_dic = {}
	k,d =  F[right_image][ts][:],F[right_image][vals][:]
	for i in range(0,len(k)-1):
		a = int(k[i]*1000)
		b = int(k[i+1]*1000)
		c = (a+b)/2
		for j in range(a,b):
			if j < c:
				v = k[i]
			else:
				v = k[i+1]
			interp_dic[j/1000.] = v
	lv = F[left_image][ts][:]
	rv = []
	try:
		for iv in rlen(lv):
			rv.append(interp_dic[lv[iv]])
	except Exception as e:
		print("********** Exception ***********************")
		print("""	try:
		for iv in rlen(lv):
			rv.append(interp_dic[lv[iv]]))
		print(e.message, e.args)
			""")
		print(e.message, e.args)
	return np.array(rv)


def Left_Timestamp_Metadata(*args):
	"""
	right timestamps . . .
	"""
	Args = args_to_dictionary(args)
	D = {}
	run_namev = Args[run_name]
	h5py_pathv = Args[h5py_path]
	True
	pathv = opj(h5py_pathv,run_namev,'original_timestamp_data.h5py')
	assert_disk_locations(pathv)

#	F = h5py.File(pathv,'r')
#	L = h5py.File(opj(pname(pathv),'left_timestamp_metadata.h5py'),'w')
	F = h5r(pathv)
	L = h5w(opj(pname(pathv),'left_timestamp_metadata.h5py'))

	L.create_dataset(ts,data=np.array(F[left_image][ts]))

	right_tsv = _assign_right_image_timestamps2(F)
	#for iv in range(len(F[left_image][vals])):
	#	right_tsv.append(F[right_image][ts][iv])

	L.create_dataset(right_ts,data=np.array(right_tsv))
	#assert( np.abs( 0.03 - np.median(L[ts][:]-L[right_ts][:]) ) < 0.01 )

	for k_ in sorted(F.keys()):
		if k_ != left_image and k_ != right_image:
			if len(F[k_][ts]) > 0:
				print('\tprocessing '+k_)
				L.create_dataset(k_,data=np.interp(L[ts][:],F[k_][ts][:],F[k_][vals][:]))
				if k_ in P[MEO_PARAMS]:
					L.create_dataset(k_+'_meo',  
						data=np.interp(L[ts][:],F[k_][ts][:],meo(F[k_][vals][:],P[MEO_PARAMS][k_])))

	L[state][:]=L[state][:].astype(int)

	left_ts_deltasv = 0.0 * L[ts][:]
	for iv in range(1,len(L[ts][:])):
		left_ts_deltasv[iv] = L[ts][iv] - L[ts][iv-1]
	L.create_dataset(left_ts_deltas,data=left_ts_deltasv)
	L.close()













rgb_1to4_path = 'rgb_1to4_path'

def Original_Timestamp_Data_from_preprocessed_data_pkl(*args):
	"""
	Translate from preprocessed_data.pkl and .pkl rosbag image files to original_timestamp_data.h5py
	"""
	Args = args_to_dictionary(args)
	preprocessed_datafile_path_ = Args[preprocessed_datafile_path]
	rgb_1to4_path_ = Args[rgb_1to4_path]
	h5py_path_ = Args[h5py_path]
	True
	run_name_ = fname(pname(preprocessed_datafile_path_))
	unix('mkdir -p '+opj(h5py_path_,run_name_))
	file_path_ = opj(h5py_path_,run_name_,'original_timestamp_data.h5py')
	if os.path.exists(file_path_):
		spd2s(file_path_+' exists, doing nothing.')
		return None

	O = lo(preprocessed_datafile_path_)
	D = {}
	for k_ in O.keys():
		D[k_] = {}
		ts_,vals_ = get_sorted_keys_and_data(O[k_])
		D[k_][ts] = np.array(ts_)
		D[k_][vals] = np.array(vals_)


	for k_ in D.keys():
		if len(shape(D[k_][vals])) == 2:
			if shape(D[k_][vals])[1] == 3:
				D[k_][vals] = np.array(D[k_][vals])
				ctr_ = 0
				for q_ in [x,y,z]:
					new_key_ = k_+'_'+q_
					D[new_key_] = {}
					D[new_key_][ts] = D[k_][ts]
					D[new_key_][vals] = D[k_][vals][:,ctr_]
					ctr_ += 1
				del D[k_]


	Temp = {}
	for side_ in ['left','right']:
		Temp[side_+'_image'] = {}
	bag_pkls_ = sggo(rgb_1to4_path_,'*.bag.pkl')
	for b_ in bag_pkls_:
		print b_
		O = load_obj(b_)
		for side_ in ['left','right']:
			ts_ = O[side_].keys()
			for t_ in ts_:
				Temp[side_+'_image'][t_] = O[side_][t_]
			ts_,vals_ = get_sorted_keys_and_data(Temp[side_+'_image'])
			D[side_+'_image'][ts] = ts_
			D[side_+'_image'][vals] = vals_


	F = h5w(file_path_)
	for topic_ in D.keys():
		print topic_
		Group = F.create_group(topic_)
		Group.create_dataset(ts,data=D[topic_][ts])
		Group.create_dataset(vals,data=D[topic_][vals])
	F.close()
	return(D)



if True:
	D =  Original_Timestamp_Data_from_preprocessed_data_pkl(
		preprocessed_datafile_path,'/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/meta/direct_local_VAL_LCR_28Jul17_10h44m46s_Mr_Yellow/preprocessed_data.pkl',
		h5py_path,opjD(),
		rgb_1to4_path,'/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/rgb_1to4/direct_local_VAL_LCR_28Jul17_10h44m46s_Mr_Yellow' )


#EOF
