from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis2 import *
import data.utils.animate as animate
import arena.planner.Markers as Markers
import arena.planner.Potential_Fields as Potential_Fields
import arena.planner.Cars as Cars
from arena.planner.Constants import C



def Other_Object(the_name,the_type):
	D = {}
	D['type'] = 'Other_Object'
	D['the_type'] = the_type
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Storing spatial information for objects of interest')
	D['the_name'] = the_name
	def _reinit():
		D['xy'] = None
		D['in_view'] = None
		D['angle'] = None
		D['dist'] = None
	D['reinit'] = _reinit
	def _process_spatial_relations(xy_our,our_heading):
		xy_other = D['xy']
		if len(xy_other) > 0:
			if our_heading != None:
				angle_to_other,distance_to_other,in_view = relation_to_other_object(our_heading,xy_our,xy_other,C['view_angle'])
				D['angle'] = angle_to_other
				D['dist'] = distance_to_other
				D['in_view'] = in_view
			else:
				return None
		else:
			return None
	D['process_spatial_relations'] = _process_spatial_relations
	return D




def setup_spatial_dics(current_run):
	marker_spatial_dic = {}
	ctr = 0
	for xy in C['markers']['xy']:
		ctr += 1
		m = Other_Object(ctr,'marker')
		m['reinit']()
		m['xy'] = xy
		marker_spatial_dic[ctr] = m

	car_spatial_dic = {}
	for n in set(C['car_names']) - set(list(current_run['our_car_name'])):
		m = Other_Object(n,'car')
		m['reinit']()
		car_spatial_dic[n] = m
	return car_spatial_dic,marker_spatial_dic




def update_spatial_dics(current_run,car_spatial_dic,marker_spatial_dic,t):
	success = current_run['our_car']['establish_valid_time_and_index'](current_run['run_name'],t)
	if success:
		xy_our = current_run['our_car']['current_xy']()
		our_heading = current_run['our_car']['current_heading']()
		list_of_other_car_trajectories = current_run['our_car']['runs'][current_run['run_name']]['list_of_other_car_trajectories']
		for l in list_of_other_car_trajectories:
			other_car_name = l[0]
			other_car_run_name = l[1]
			success = current_run['cars'][other_car_name]['establish_valid_time_and_index'](other_car_run_name,t)
			car_spatial_dic[other_car_name]['reinit']()
			if success:
				xy = current_run['cars'][other_car_name]['current_xy']()	
				heading = current_run['cars'][other_car_name]['current_heading']()
				car_spatial_dic[other_car_name]['xy'] = xy
				car_spatial_dic[other_car_name]['process_spatial_relations'](xy_our,our_heading)

		for m in marker_spatial_dic.keys():
			marker_spatial_dic[m]['process_spatial_relations'](xy_our,our_heading)
		return True
	else:
		return False

	

def relation_to_other_object(our_heading,xy_our,xy_other,view_angle):
	in_view = False
	angle_to_other = angle_clockwise(our_heading,array(xy_other)-array(xy_our))
	if angle_to_other > 360-view_angle:
		angle_to_other = angle_to_other-360
	distance_to_other = length(xy_other-xy_our)
	if angle_to_other > -view_angle and angle_to_other < view_angle:
		in_view = True
	return angle_to_other,distance_to_other,in_view



def objects_to_angle_distance_representation(reference_angles,other_angle_distance_list,are_markers=False):
	m = array(reference_angles)*0.0
	if len(reference_angles) > len(other_angle_distance_list) and not are_markers:
		for object_angle,object_distance in other_angle_distance_list:
			indx = find_index_of_closest(object_angle,reference_angles)
			if m[indx] < 1/object_distance:
				m[indx] = 1/object_distance
	else:
		other_angle_distance_array = array(other_angle_distance_list)
		other_angles = other_angle_distance_array[:,0]
		other_distances = other_angle_distance_array[:,1]
		for i in range(len(reference_angles)):
			indx = find_index_of_closest(reference_angles[i],other_angles)
			m[i] = 1/other_distances[indx]
	return m


def get_angle_distance_view(current_run,spatial_dic,are_markers=False):
	other_angle_distance_list = []
	angle_dist_view = []
	for c in current_run[spatial_dic].keys():
		if current_run[spatial_dic][c]['in_view']:
			other_angle_distance_list.append([current_run[spatial_dic][c]['angle'],current_run[spatial_dic][c]['dist']])
	if len(other_angle_distance_list) > 0:
		angle_dist_view = objects_to_angle_distance_representation(C['view_angles'],other_angle_distance_list,are_markers)
	return angle_dist_view


def get_sample_points(pts,angles,pfield,heading):
	sample_points = []
	potential_values = []
	heading = heading.copy()
	heading *= 0.5 # 50 cm, about the length of the car
	for the_arena in angles:
		sample_points.append( rotatePoint([0,0],heading,the_arena) )
	for sp in sample_points:
		pix = pfield['Image']['floats_to_pixels']([sp[0]+array(pts)[0],sp[1]+array(pts)[1]])
		potential_values.append(pfield['Image']['img'][pix[0],pix[1]])
		#pfield['Image']['img'][pix[0],pix[1]] = 1 # for checking
	return potential_values


def interpret_potential_values(potential_values):
	min_potential_index = potential_values.index(min(potential_values))
	max_potential_index = potential_values.index(max(potential_values))
	middle_index = int(len(potential_values)/2)
	potential_values = array(potential_values)
	pmin = potential_values.min()
	pmax = potential_values.max()
	potential_values = z2o(potential_values) * pmax
	d = 99.0/(1.0*len(potential_values)-1)
	steer_angles = np.floor(99-arange(0,100,d))
	p = min(pmax/0.8,1.0)
	steer = int((p*steer_angles[min_potential_index]+(1-p)*49.0))
	return steer


