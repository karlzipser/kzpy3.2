from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis import *
import data.utils.animate as animate
import arena.planner.Markers as Markers
import arena.planner.Potential_Fields as Potential_Fields
import arena.planner.Cars as Cars



def Spatial_Configurations(run_name):

	def _compute(t)
		xy_our = cars[our_car]['report_camera_positions'](run_name,t)

		other_cars_xy_list = []
		other_cars_in_view_xy_list = []
		other_cars_angle_distance_list = []
		other_cars_in_view_angle_distance_list = []

		markers_xy_list = []
		markers_angle_distance_list = []
		markers_in_view_xy_list = []
		markers_in_view_angle_distance_list = []

		no_cars_in_view = True
		no_markers_in_view = True

		if len(xy_our) > 0:
			xy_our = array(xy_our)
			our_heading = cars[our_car]['state_info']['heading']
			for l in list_of_other_car_trajectories:
				other_car_name = l[0]
				other_car_run_name = l[1]
				xy_other = cars[other_car_name]['report_camera_positions'](other_car_run_name,t)
				if len(xy_other) > 0:
					if our_heading != None:
						angle_to_other,distance_to_other,in_view = relation_to_other_object(our_heading,xy_our,xy_other,view_angle)
						other_cars_angle_distance_list.append([angle_to_other,distance_to_other])
						other_cars_xy_list.append(xy_other)
						other_cars_angle_distance_list.append([angle_to_other,distance_to_other])
						if in_view:
							no_cars_in_view = False
							other_cars_in_view_angle_distance_list.append([angle_to_other,distance_to_other])
							other_cars_in_view_xy_list.append(xy_other)
			for xy_other in markers['xy']:
				if len(xy_other) > 0:
					if our_heading != None:
						angle_to_other,distance_to_other,in_view = relation_to_other_object(our_heading,xy_our,xy_other,view_angle)
						markers_angle_distance_list.append([angle_to_other,distance_to_other])
						markers_xy_list.append(xy_other)
						markers_angle_distance_list.append([angle_to_other,distance_to_other])
						markers_xy_list.append(xy_other)
						if in_view:
							no_markers_in_view = False
							markers_in_view_angle_distance_list.append([angle_to_other,distance_to_other])
							markers_in_view_xy_list.append(xy_other)




def relation_to_other_object(our_heading,xy_our,xy_other,view_angle):
	in_view = False
	angle_to_other = angle_clockwise(our_heading,array(xy_other)-array(xy_our))
	if angle_to_other > 360-view_angle:
		angle_to_other = angle_to_other-360
	distance_to_other = length(xy_other-xy_our)
	if angle_to_other > -view_angle and angle_to_other < view_angle:
		in_view = True
	return angle_to_other,distance_to_other,in_view



def objects_to_angle_distance_representation(reference_angles,other_angle_distance_list):
	m = array(reference_angles)*0.0
	if len(reference_angles) > len(other_angle_distance_list):
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






