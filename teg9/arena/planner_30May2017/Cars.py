from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis import *
import data.utils.general
from data.utils.general import car_name_from_run_name
from data.utils.general import car_colors as colors
import arena.planner.Potential_Fields as Potential_Fields


def Car(N,car_name,origin,mult,markers):
	D = {}
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Car object.')
	D['car_name'] = car_name
	D['potential_field'] = Potential_Fields.Arena_Potential_Field(origin,mult,markers)
	D['runs'] = {}
	D['n_for_heading'] = 15
	for run_name in N[car_name].keys():
		D['runs'][run_name] = {}
		R = D['runs'][run_name]
		R['trajectory'] = N[car_name][run_name]['self_trajectory']
		R['list_of_other_car_trajectories'] = []
		"""
			for ot in N[car_name][run_name]['other_trajectories']:
				other_run_name = ot['run_name']
				other_car_name = car_name_from_run_name(other_run_name)
				R['list_of_other_car_trajectories'].append( [other_car_name,other_run_name] )
		"""		
		for other_run_name in N[car_name][run_name]['other_trajectories']:
			other_car_name = car_name_from_run_name(other_run_name)
			R['list_of_other_car_trajectories'].append( [other_car_name,other_run_name] )

	def _rewind():
		D['state_info'] = {}
		#D['state_info']['positions'] = {}
		D['state_info']['near_i'] = 0
		D['state_info']['near_t'] = 0
		D['state_info']['near_t_prev'] = 0
		D['state_info']['pts'] = []
		D['state_info']['heading'] = None
		D['state_info']['heading_prev'] = 0
		D['state_info']['relative_heading'] = 90
	D['rewind'] = _rewind


	def _check_trajectory_point(traj,side,i,t):
		assert(traj['ts'][i] <= t)
		if traj['ts'][i] == t:
			if traj[side]['t_vel'][i] > 2: # 1.788: # Above 4 mph
				return False
			if traj[side]['t_vel'][i]<0.2: #TEMP
				return False
			elif traj['camera_separation'][i] > 0.25: # almost larger than length of car
				return False
			elif traj[side]['timestamp_gap'][i] > 0.1: # missed data points
				return False
			elif length([traj[side]['x'][i],traj[side]['y'][i]]) > length(markers['xy'][0]):
				return False
			return True
		assert(False)


	def _valid_time_and_index(run_name,t):
		traj = D['runs'][run_name]['trajectory']
		if t>traj['ts'][0] and t<traj['ts'][-1]:
			near_t = -1
			for i in range(D['state_info']['near_i'],len(traj['ts'])):
				if traj['ts'][i-1]<t and traj['ts'][i]>t:
					near_t = traj['ts'][i]
					near_i = i
					break
			if near_t > 0:
				D['state_info']['near_i'] = near_i
				D['state_info']['near_t'] = near_t
				for side in ['left','right']:
					if not _check_trajectory_point(traj,side,near_i,near_t):
						return False,False
				return near_t,near_i
		return False,False


	def _report_camera_positions(run_name,t):
		near_t,near_i = _valid_time_and_index(run_name,t)
		if not near_t:
			return []
		traj = D['runs'][run_name]['trajectory']
		positions = []
		for side in ['left','right']:
			positions.append([traj[side]['x'][near_i],traj[side]['y'][near_i]])
		D['state_info']['pts'].append(array(positions).mean(axis=0))

		if len(D['state_info']['pts']) >= D['n_for_heading']:
			n = D['n_for_heading']
			D['state_info']['heading'] = normalized_vector_from_pts(D['state_info']['pts'][-n:])
			if D['state_info']['pts'][-n][0] > D['state_info']['pts'][-1][0]:
				D['state_info']['heading'] *= -1
			if D['state_info']['near_t'] - D['state_info']['near_t_prev'] < 0.1:
				if np.degrees(angle_between(D['state_info']['heading'],D['state_info']['heading_prev'])) > 45:
					#print_stars()
					#print('Heading warning!!!')
					#print_stars()
					D['state_info']['heading'] = D['state_info']['heading_prev']
			D['state_info']['relative_heading'] = (degrees(angle_between(D['state_info']['heading'],D['state_info']['pts'][-1])))
			D['state_info']['heading_prev'] = D['state_info']['heading']
			D['state_info']['near_t_prev'] = D['state_info']['near_t']
		else:
			D['state_info']['heading'] = None
		return D['state_info']['pts'][-1] #positions
	D['report_camera_positions'] = _report_camera_positions

	"""
	def _report_camera_positions(run_name,t):
		near_t,near_i = _valid_time_and_index(run_name,t)
		if not near_t:
			return False
		traj = D['runs'][run_name]['trajectory']
		positions = []
		for side in ['left','right']:
			positions.append([traj[side]['x'][near_i],traj[side]['y'][near_i]])
			D['state_info']['pts'].append(positions[0])

			if len(D['state_info']['pts']) >= D['n_for_heading']:
				n = D['n_for_heading']
				D['state_info']['heading'] = normalized_vector_from_pts(D['state_info']['pts'][-n:])
				if D['state_info']['pts'][-n][0] > D['state_info']['pts'][-1][0]:
					D['state_info']['heading'] *= -1
			else:
				D['state_info']['heading'] = None
		return positions
	D['report_camera_positions'] = _report_camera_positions
	"""

	def _get_left_image(run_name):
		traj = D['runs'][run_name]['trajectory']
		index = traj['data']['t_to_indx'][D['state_info']['near_t']]
		img = traj['data']['left'][index]
		return img
	D['get_left_image'] = _get_left_image

	def _get_right_image(run_name):
		traj = D['runs'][run_name]['trajectory']
		index = traj['data']['t_to_indx'][D['state_info']['near_t']]
		img = traj['data']['right'][index]
		return img
	D['get_right_image'] = _get_right_image


	def _load_image_and_meta_data(run_name,bair_car_data_location):
		import data.utils.general
		import data.utils.multi_preprocess_pkl_files_1_1
		bag_folders_dst_rgb1to4_path = opj(bair_car_data_location,'rgb_1to4')
		bag_folders_dst_meta_path = opj(bair_car_data_location,'meta')
		D['runs'][run_name]['trajectory']['data'] = data.utils.general.get_new_Data_dic()
		data.utils.multi_preprocess_pkl_files_1_1.multi_preprocess_pkl_files(
			D['runs'][run_name]['trajectory']['data'],
				opj(bag_folders_dst_meta_path,run_name),
				opj(bag_folders_dst_rgb1to4_path,run_name),
				print_b=True,
				load_right_images=True)
	D['load_image_and_meta_data'] = _load_image_and_meta_data


	return D







