from Parameters_Module import *
exec(identify_file_str)
from kzpy3.vis2 import *

import sensor_msgs.point_cloud2
#from sensor_msgs.msg import PointCloud2

def Original_Timestamp_Data(bag_folder_path=None, h5py_path=None):
	"""
	Translate from .bag files to original_timestamp_data.h5py
	"""
	D = {}
	DA = {}
	bag_folder_pathv = bag_folder_path
	h5py_pathv = h5py_path
	True
	run_namev = fname(bag_folder_pathv)
	unix('mkdir -p '+opj(h5py_pathv,run_namev))
	file_path = opj(h5py_pathv,run_namev,'original_timestamp_data.h5py')
	if os.path.exists(file_path):
		spd2s(file_path+' exists, doing nothing.')
		return None
	import rospy
	import rosbag
	import cv2
	import cv_bridge
	from cv_bridge import CvBridge, CvBridgeError
	bridge = cv_bridge.CvBridge()

	image_topicsv = ['zed/left/image_rect_color','zed/right/image_rect_color']
	single_value_topicsv = P['SINGLE_VALUE_TOPICS']
	vector3_topicsv = P['VECTOR3_TOPICS']
	string_topics = P['STRING_TOPICS']
	all_topics_ = image_topicsv + single_value_topicsv + vector3_topicsv + string_topics
	bair_all_topics_ = []
	for v in all_topics_:
		if v != 'points':
			bair_all_topics_.append('/bair_car/'+v)
		else:
			bair_all_topics_.append('/os1_node/points')
	Rename = {}
	Rename['zed/left/image_rect_color'] = 'left_image'
	Rename['zed/right/image_rect_color'] = 'right_image'
	Rename['cmd/heading_pause'] = 'heading_pause'
	Rename['cmd/car_in_range'] = 'car_in_range'
	Rename['cmd/motor'] = 'cmd_motor'
	Rename['cmd/steer'] = 'cmd_steer'

	for topic_ in all_topics_:
		if 'zed' in topic_ or 'cmd' in topic_:
			topic_ = Rename[topic_]
			if P['USE_ARUCO']:
				if 'left' in topic_ or 'right' in topic_:
					DA[topic_+'_aruco'] = {}
					DA[topic_+'_aruco']['ts'] = []
					DA[topic_+'_aruco']['vals'] = []
		D[topic_] = {}
		D[topic_]['ts'] = []
		D[topic_]['vals'] = []

	bag_filesv = sorted(glob.glob(opj(bag_folder_pathv,'*.bag')))
	
	cprint(d2s('Processing',len(bag_filesv),'bag files:'),'red')
	for bv in bag_filesv:
		cprint('\t'+bv,'blue')

	timerv = Timer(0)

	for bv in bag_filesv:

		timerv.reset()

		cprint(bv,'yellow')

		bagv = rosbag.Bag(bv)

		for m_ in bagv.read_messages(topics=bair_all_topics_):
			timestampv = round(m_[2].to_time(),3) # millisecond resolution
			assert(is_number(timestampv))


			topic_ = m_[0].replace('/bair_car/','')

			topic_ = topic_.replace('/os1_node/','')

			if 'zed' in m_[0]:
				valv = bridge.imgmsg_to_cv2(m_[1],"rgb8")
				valv = cv2.resize(valv, (0,0), fx=0.25, fy=0.25)
				if P['USE_ARUCO']:
					ad = _get_aruco_data(valv)
					DA[Rename[topic_]+'_aruco']['ts'].append(timestampv) 			
					DA[Rename[topic_]+'_aruco']['vals'].append(ad)
			elif m_[0] == 'points':	
				try:
					# https://answers.ros.org/question/240491/point_cloud2read_points-and-then/
					valv = list(sensor_msgs.point_cloud2.read_points(m_[1],skip_nans=True,field_names=("x","y","z")))
				except  Exception as e:
				    exc_type, exc_obj, exc_tb = sys.exc_info()
				    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				    CS_('Exception!',emphasis=True)
				    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
				    raw_enter()
			elif topic_ in string_topics:
				#print topic_,type(m_[1].data),m_[1].data
				valv = P['string_to_num_dic'][topic_][m_[1].data]
				#print valv
			elif hasattr(m_[1], 'data'):
				if is_number(m_[1].data):
					valv = m_[1].data
			elif hasattr(m_[1], 'x'):
				valv = [m_[1].x,m_[1].y,m_[1].z]
				#print m_[1]
				for nv in valv:
					assert(is_number(nv))
			elif hasattr(m_[1], 'latitude'):
				valv = [m_[1].latitude,m_[1].longitude,m_[1].altitude]
				for nv in valv:
					assert(is_number(nv))
			else:
				raise ValueError('ERROR because: topic '+topic_+' not processed.')
			if 'zed' in topic_ or 'cmd' in topic_:
				topic_ = Rename[topic_]

			D[topic_]['ts'].append(timestampv)
			D[topic_]['vals'].append(valv)

		print(d2s('\t',dp(timerv.time()),'seconds'))

	for k_ in D.keys():
		if len(shape(D[k_]['vals'])) == 2:
			if shape(D[k_]['vals'])[1] == 3:
				D[k_]['vals'] = np.array(D[k_]['vals'])
				ctr_ = 0
				for q_ in ['x','y','z']:
					new_key_ = k_+'_'+q_
					D[new_key_] = {}
					D[new_key_]['ts'] = D[k_]['ts']
					D[new_key_]['vals'] = D[k_]['vals'][:,ctr_]
					ctr_ += 1
				del D[k_]

	F = h5w(file_path)
	pd2s('Topics:')
	for topic_ in D.keys():
		#print topic_
		pd2s('\t',topic_,len(D[topic_]['ts']))
		Group = F.create_group(topic_)
		Group.create_dataset('ts',data=D[topic_]['ts'])
		Group.create_dataset('vals',data=D[topic_]['vals'])
	F.close()
	if P['USE_ARUCO']:
		so(opj(h5py_pathv,run_namev,'aruco_data.pkl'),DA)
	return(D)



def _assign_right_image_timestamps2(F):
	interp_dic = {}
	k,d =  F['right_image']['ts'][:],F['right_image']['vals'][:]
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
	lv = F['left_image']['ts'][:]
	rv = []
	for iv in rlen(lv):
		#print iv
		try:
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



def Left_Timestamp_Metadata(run_name=None,h5py_path=None):
	D = {}
	run_namev = run_name
	h5py_pathv = h5py_path

	if os.path.exists(opj(h5py_pathv,run_namev,'left_timestamp_metadata_right_ts.h5py')):
		spd2s(opj(h5py_pathv,run_namev,'left_timestamp_metadata_right_ts.h5py')+' exists, doing nothing.')
		return None
	pathv = opj(h5py_pathv,run_namev,'original_timestamp_data.h5py')
	assert_disk_locations(pathv)

	F = h5r(pathv)
	L = h5w(opj(pname(pathv),'left_timestamp_metadata_right_ts.h5py'))

	L.create_dataset('ts',data=np.array(F['left_image']['ts']))

	right_tsv = _assign_right_image_timestamps2(F)

	L.create_dataset('right_ts',data=np.array(right_tsv))

	for k_ in sorted(F.keys()):
		if k_ != 'left_image' and k_ != 'right_image':
			if len(F[k_]['ts']) > 0:
				print('\tprocessing '+k_)
				L.create_dataset(k_,data=np.interp(L['ts'][:],F[k_]['ts'][:],F[k_]['vals'][:]))
				if k_ in P['MEO_PARAMS']:
					L.create_dataset(k_+'_meo',  
						data=np.interp(L['ts'][:],F[k_]['ts'][:],meo(F[k_]['vals'][:],P['MEO_PARAMS'][k_])))
	if 'state' in L:
		if len(L['state']) > 0:
			L['state'][:]=L['state'][:].astype(int)

	left_ts_deltasv = 0.0 * L['ts'][:]
	for iv in range(1,len(L['ts'][:])):
		left_ts_deltasv[iv] = L['ts'][iv] - L['ts'][iv-1]
	L.create_dataset('left_ts_deltas',data=left_ts_deltasv)
	L.close()



def make_flip_images(h5py_folder=None):
	h5py_folder_ = h5py_folder

	f_ = opj(h5py_folder_,'flip_images.h5py')
	if os.path.exists(f_):
		spd2s(f_+' exists, doing nothing.')
		return None
	O = h5r(opj(h5py_folder_,'original_timestamp_data.h5py'))
	F = h5w(f_)
	for topic_ in ['left_image','right_image']:
		flip_topic_ = topic_+'_flip'
		pd2s('\t',topic_,'to',flip_topic_)
		flip_images_ = []
		for i_ in range(len(O[topic_]['ts'])):
			flip_images_.append(cv2.flip(O[topic_]['vals'][i_],1))
		flip_images_ = np.array(flip_images_)
		Group = F.create_group(flip_topic_)
		Group.create_dataset('ts',data=O[topic_]['ts'])
		Group.create_dataset('vals',data=flip_images_)
	F.close()



if P['USE_ARUCO']:
	import kzpy3.misc.data_analysis.Angle_Dict_Creator as Angle_Dict_Creator
	def _get_aruco_data(img=None):
		Q = {}
		if True:#try:
			mm = {}
			angles_to_center_more = {}
			angles_surfaces_more = {}
			distances_marker_more = {}
			for r in range(2):
				angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(img,borderColor=None)
				for k in angles_to_center.keys():
					if k not in angles_to_center_more.keys():
						angles_to_center_more[k] = []
						angles_surfaces_more[k] = []
						distances_marker_more[k] = []
					angles_to_center_more[k].append(angles_to_center[k])
					angles_surfaces_more[k].append(angles_surfaces[k])
					distances_marker_more[k].append(distances_marker[k])
			for k in angles_to_center_more.keys():
				angles_to_center[k] = na(angles_to_center_more[k]).mean()
				angles_surfaces[k] = na(angles_surfaces_more[k]).mean() #!!!
				distances_marker[k] = na(distances_marker_more[k]).mean() #!!!

			Q = {'angles_to_center':angles_to_center,'angles_surfaces':angles_surfaces,'distances_marker':distances_marker}
		else:#except Exception as e:
			print("********** Exception 123 ***********************")
			print(e.message, e.args)
			#timer.message(d2s(i,'views =',views,int(100*i/(1.0*n)),'%'),color='white')
		return Q









#EOF
