from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis2 import *
import data.utils.general
from data.utils.general import car_name_from_run_name
from arena.planner.Constants import C


def Car(N,car_name,origin,mult,markers):
	D = {}
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Car object.')
	D['car_name'] = car_name
	D['type'] = 'Car'
	D['runs'] = {}
	D['n_for_heading'] = C['n_for_heading']
	for run_name in N[car_name].keys():
		D['runs'][run_name] = {}
		R = D['runs'][run_name]
		R['trajectory'] = N[car_name][run_name]['self_trajectory']
		R['list_of_other_car_trajectories'] = []	
		for other_run_name in N[car_name][run_name]['other_trajectories']:
			other_car_name = car_name_from_run_name(other_run_name)
			R['list_of_other_car_trajectories'].append( [other_car_name,other_run_name] )
	print("""
		Remeber to smooth velocities and look at encoder values.
		Also look at raw trajectories.
		Also time to collision.
		Clockwise?
	""")

	def _rewind():
		D['state_info'] = {}
		D['state_info']['near_i'] = 0
		D['state_info']['near_t'] = 0
		D['state_info']['near_t_prev'] = 0
		D['state_info']['pts'] = []
		D['state_info']['heading'] = None
		D['state_info']['heading_prev'] = [0,1]
		D['state_info']['relative_heading'] = 90
		D['state_info']['velocity'] = 0
	D['rewind'] = _rewind
	D['rewind']()


	def _report_camera_positions(run_name,t):
		near_t,near_i = _valid_time_and_index(run_name,t)
		if not near_t:
			return []
		traj = D['runs'][run_name]['trajectory']
		positions = []
		for side in ['left','right']:
			positions.append([traj[side]['x'][near_i],traj[side]['y'][near_i]])
		D['state_info']['pts'].append(array(positions).mean(axis=0))
		if len(D['state_info']['pts']) > 3*D['n_for_heading']:
			D['state_info']['pts'] = D['state_info']['pts'][-2*D['n_for_heading']:]
		if len(D['state_info']['pts']) >= D['n_for_heading']:
			n = D['n_for_heading']
			D['state_info']['heading'] = normalized_vector_from_pts(D['state_info']['pts'][-n:])
			#print(d2s('>',length(D['state_info']['heading'])))
			if D['state_info']['pts'][-n][0] > D['state_info']['pts'][-1][0]:
				D['state_info']['heading'] *= -1.0
			#print(d2s('>.',length(D['state_info']['heading'])))
			#print(d2s('<',length(D['state_info']['heading_prev'])))
			if D['state_info']['near_t'] - D['state_info']['near_t_prev'] < 0.1:
				if np.degrees(angle_between(D['state_info']['heading'],D['state_info']['heading_prev'])) > 45:
					#print_stars()
					#print('Heading warning!!!')
					#print_stars()
					#print(d2s('>..',length(D['state_info']['heading'])))
					D['state_info']['heading'] = D['state_info']['heading_prev']
					#print(d2s('>...',length(D['state_info']['heading'])))
			D['state_info']['relative_heading'] = (angle_clockwise(D['state_info']['heading'],D['state_info']['pts'][-1]))
			D['state_info']['heading_prev'] = D['state_info']['heading'].copy()
			D['state_info']['near_t_prev'] = D['state_info']['near_t']
			D['state_info']['velocity'] = (traj['left']['t_vel']+traj['right']['t_vel'])/2.0

		else:
			D['state_info']['heading'] = None
		#if D['state_info']['heading'] != None:
			#print(d2s('>....',length(D['state_info']['heading'])))
		return (D['state_info']['pts'][-1],D['state_info']['heading']) #positions
	D['report_camera_positions'] = _report_camera_positions


	def _check_trajectory_point(traj,side,i,t):
		assert(traj['ts'][i] <= t)
		if traj['ts'][i] == t:
			if traj[side]['t_vel'][i] > 3: # 1.788: # Above 4 mph
				print "traj[side]['t_vel'][i] > 3"
				return False
			if traj[side]['t_vel'][i]<0.1: #TEMP
				print "raj[side]['t_vel'][i]<0.1"
				return False
			elif traj['camera_separation'][i] > 0.5: # almost larger than length of car
				print "traj['camera_separation'][i] > 0.5"
				return False
			elif traj[side]['timestamp_gap'][i] > 0.5: # missed data points
				print "traj[side]['timestamp_gap'][i] > 0.5"
				return False
			elif length([traj[side]['x'][i],traj[side]['y'][i]]) > length(markers['xy'][0]):
				print "length([traj[side]['x'][i],traj[side]['y'][i]]) > length(markers['xy'][0])"
				return False
			return True
		assert(False)

	def __check_trajectory_point(traj,side,i,t):
		assert(traj['ts'][i] <= t)
		if traj['ts'][i] == t:
			if traj[side]['t_vel'][i] > 3: # 1.788: # Above 4 mph
				return False
			if traj[side]['t_vel'][i]<0.1: #TEMP
				return False
			elif traj['camera_separation'][i] > 0.5: # almost larger than length of car
				return False
			elif traj[side]['timestamp_gap'][i] > 0.5: # missed data points
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
				if traj['ts'][i-1]<t and traj['ts'][i]>=t:
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


	def _get_image(run_name,side):
		traj = D['runs'][run_name]['trajectory']
		index = traj['data']['t_to_indx'][D['state_info']['near_t']]
		img = traj['data'][side][index]
		return img		
	D['get_image'] = _get_image


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

<<<<<<< HEAD:teg9/arena/planner_4June2017_new_direction/Cars.py



	def _get_sample_points(pts,angles,pfield,heading):
	    sample_points = []
	    potential_values = []
	    heading *= 0.5 # 50 cm, about the length of the car
	    for the_arena in angles:
	        sample_points.append( rotatePoint([0,0],heading,the_arena) )
	    for k in range(len(sample_points)):
	        f = sample_points[k]
	    for sp in sample_points:
	    	if GRAPHICS:
	    		pfield['Image']['plot_pts'](array(sp)+array(pts[-1,:]),'g')
	        pix = pfield['Image']['floats_to_pixels']([sp[0]+pts[-1,0],sp[1]+pts[-1,1]])
	        potential_values.append(pfield['Image']['img'][pix[0],pix[1]])
	    return sample_points,potential_values

	def _interpret_potential_values(potential_values):
		min_potential_index = potential_values.index(min(potential_values))
		max_potential_index = potential_values.index(max(potential_values))
		middle_index = int(len(potential_values)/2)
		potential_values = array(potential_values)
		pmin = potential_values.min()
		pmax = potential_values.max()
		potential_values = z2o(potential_values) * pmax
		if GRAPHICS:
			figure(9);plot(potential_values,'bo-')
		d = 99.0/(1.0*len(potential_values)-1)
		steer_angles = np.floor(99-arange(0,100,d))
		p = min(pmax/0.8,1.0)
		steer = int((p*steer_angles[min_potential_index]+(1-p)*49.0))
		return steer



=======
	print("created "+D['type']+": "+D['car_name'])
>>>>>>> 469d5a9c765b60a9a207da832eb2a9470afff21b:teg9/arena/planner/Cars.py
	return D







