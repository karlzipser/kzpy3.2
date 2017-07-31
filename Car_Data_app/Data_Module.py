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
		print(stars0v+file_path+' exists, doing nothing.'+stars1v)
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

	#temp_counter = 0
	for bv in bag_filesv:
		#if temp_counter >= 2:
		#	break
		#temp_counter += 1
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

	for kv in D.keys():
		if len(shape(D[kv][vals])) == 2:
			if shape(D[kv][vals])[1] == 3:
				D[kv][vals] = np.array(D[kv][vals])
				ctrv = 0
				for qv in [x,y,z]:
					new_keyv = kv+'_'+qv
					D[new_keyv] = {}
					D[new_keyv][ts] = D[kv][ts]
					D[new_keyv][vals] = D[kv][vals][:,ctrv]
					ctrv += 1
				del D[kv]

#	F = h5py.File(file_path,'w')
	F = h5w(file_path)
	for topicv in D.keys():
		print topicv
		Group = F.create_group(topicv)
		Group.create_dataset(ts,data=D[topicv][ts])
		Group.create_dataset(vals,data=D[topicv][vals])
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
    for iv in rlen(lv):
    	rv.append(interp_dic[lv[iv]])
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

	for kv in sorted(F.keys()):
		if kv != left_image and kv != right_image:
			if len(F[kv][ts]) > 0:
				print('\tprocessing '+kv)
				L.create_dataset(kv,data=np.interp(L[ts][:],F[kv][ts][:],F[kv][vals][:]))
				if kv in P[MEO_PARAMS]:
					L.create_dataset(kv+'_meo',  
						data=np.interp(L[ts][:],F[kv][ts][:],meo(F[kv][vals][:],P[MEO_PARAMS][kv])) )

	L[state][:]=L[state][:].astype(int)

	left_ts_deltasv = 0.0 * L[ts][:]
	for iv in range(1,len(L[ts][:])):
		left_ts_deltasv[iv] = L[ts][iv] - L[ts][iv-1]
	L.create_dataset(left_ts_deltas,data=left_ts_deltasv)
	L.close()




#EOF
