from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis2 import *
import data.utils.animate as animate
import arena.planner.Potential_Fields as Potential_Fields
import arena.planner.Cars as Cars
from data.utils.general import car_name_from_run_name
from arena.planner.Constants import C
import arena.planner.Spatial_Relations as Spatial_Relations



def Run(run_name,cars,the_arena,bair_car_data_location):
	D = {}
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Run object.')
	D['run_name'] = run_name
	D['cars'] = cars
	D['our_car_name'] = car_name_from_run_name(run_name)
	our_car_name = D['our_car_name']
	D['our_car'] = cars[our_car_name]
	our_car = D['our_car']
	D['the_arena'] = the_arena

	if len(gg(opjD(bair_car_data_location,'meta',run_name,'*'))) < 5: #'caffe2_z2_color_direct_local_01Jan13_00h01m07s_Mr_Yellow' in run_name:
			print("len(gg(opjD(bair_car_data_location,'meta',run_name,'*'))) < 5")
			return False
	traj = our_car['runs'][run_name]['trajectory']
	D['T0'] = traj['ts'][0]
	D['Tn'] = traj['ts'][-1]
	D['list_of_other_car_trajectories'] = our_car['runs'][run_name]['list_of_other_car_trajectories']
	def _rewind():
		for c in C['car_names']:
			D['cars'][c]['rewind']()
	D['rewind'] = _rewind

	try:
		our_car['load_image_and_meta_data'](run_name,bair_car_data_location)
	except Exception as e:
		print("********** Exception *** cars[our_car]['load_image_and_meta_data'](run_name,bair_car_data_location) ********************")
		print(our_car_name,run_name)
		print(e.message, e.args)
		return False
	car_spatial_dic,marker_spatial_dic = Spatial_Relations.setup_spatial_dics(D)
	D['car_spatial_dic'] = car_spatial_dic
	D['marker_spatial_dic'] = marker_spatial_dic
	D['rewind']()
	return D

"""
def show_arena_with_cars(current_run,an_arena,t):
	car_spatial_dic,marker_spatial_dic = current_run['car_spatial_dic'],current_run['marker_spatial_dic']
	Spatial_Relations.update_spatial_dics(current_run,car_spatial_dic,marker_spatial_dic,t)
	if len(current_run['our_car']['state_info']['pts']) > 0:
		xy = current_run['our_car']['state_info']['pts'][-1]
		if len(xy) > 0:
			an_arena['show']()
			an_arena['Image']['pts_plot'](xy,'r')
			heading = current_run['our_car']['state_info']['heading']
			if heading != None:
				an_arena['Image']['pts_plot'](xy+heading,'c')
			for c in car_spatial_dic.keys():
				if car_spatial_dic[c]['xy'] != None:
					if car_spatial_dic[c]['in_view']:
						dot_color = 'y'
					else:
						dot_color = 'b'
					an_arena['Image']['pts_plot'](car_spatial_dic[c]['xy'],dot_color)
			for c in marker_spatial_dic.keys():
				if marker_spatial_dic[c]['xy'] != None:
					if marker_spatial_dic[c]['in_view']:
						an_arena['Image']['pts_plot'](marker_spatial_dic[c]['xy'],'g')
			#print current_run['our_car']['state_info']['heading']
			pause(0.00001)
"""
def show_arena_with_cars(current_run,an_arena,t):
	car_spatial_dic,marker_spatial_dic = current_run['car_spatial_dic'],current_run['marker_spatial_dic']
	#Spatial_Relations.update_spatial_dics(current_run,car_spatial_dic,marker_spatial_dic,t)
	if len(current_run['our_car']['state_info']['pts']) > 0:
		xy = current_run['our_car']['state_info']['pts'][-1]
		if len(xy) > 0:
			an_arena['show']()
			an_arena['Image']['pts_plot'](xy,'r')
			heading = current_run['our_car']['state_info']['heading']
			
			if heading != None:
				an_arena['Image']['pts_plot'](xy+heading,'c')
			for c in car_spatial_dic.keys():
				if car_spatial_dic[c]['xy'] != None:
					if car_spatial_dic[c]['in_view']:
						dot_color = 'y'
					else:
						dot_color = 'b'
					an_arena['Image']['pts_plot'](car_spatial_dic[c]['xy'],dot_color)
			for c in marker_spatial_dic.keys():
				if marker_spatial_dic[c]['xy'] != None:
					if marker_spatial_dic[c]['in_view']:
						an_arena['Image']['pts_plot'](marker_spatial_dic[c]['xy'],'g')
			#print current_run['our_car']['state_info']['heading']
			pause(0.00001)

"""
					
	def _step(t,other_cars_in_view_xy_list,xy_our,other_cars_angle_distance_list,view_angles):	
		our_car = D['cars'][D['our_car']]		
		D['t_prev'] = t

		D['the_arena']['other_cars'](other_cars_in_view_xy_list,D['the_arena']['type'],xy_our)

		if our_car['state_info']['heading'] != None:
			sample_points,potential_values = get_sample_points(array(cars[our_car]['state_info']['pts']),angles,the_arena,cars[our_car]['state_info']['heading'])
			if D['the_arena']['type'] == 'Follow_Arena_Potential_Field':
				for ang,dist in other_cars_angle_distance_list:
					indx = find_index_of_closest(-ang,angles)
					if dist > 1:
						potential_values[indx] *= (dist-1)/8.0

			steer = interpret_potential_values(potential_values)
			real_steer = our_car['runs'][run_name]['trajectory']['data']['steer'][our_car['state_info']['near_i']]

			vel = velocity[our_car['state_info']['near_i']]
			
			n=objects_to_angle_distance_representation(view_angles,other_cars_in_view_angle_distance_list)
			m=objects_to_angle_distance_representation(view_angles,markers_angle_distance_list)

		img_left = cars[our_car]['get_image'](run_name,'left')
		img_right = cars[our_car]['get_image'](run_name,'right')
		img = img_left.copy()
		k = animate.prepare_and_show_or_return_frame(img=img,steer=steer,motor=None,state=1,delay=1,scale=2,color_mode=cv2.COLOR_RGB2BGR,window_title='plan')
		steer = 49
		if type(img_left_previous) != bool:
			imgs = {}
			imgs['left'] = [img_left_previous,img_left]
			imgs['right'] = [img_right_previous,img_right]
			ctr = 0
			for c in range(3):
				for camera in ['left','right']:
					for t in range(2):
						solver.net.blobs['ZED_data_pool2'].data[0,ctr,:,:] = imgs[camera][t][:,:,c]
						ctr += 1
			solver.net.forward()
			steer = 100*solver.net.blobs['ip2'].data[0,9]
		img = img_left.copy()
		vel = solver.net.blobs['ip_velocity'].data[-1,:][0]
		#k = animate.prepare_and_show_or_return_frame(img=img,steer=steer,motor=20.0*vel+49,state=6,delay=1,scale=2,color_mode=cv2.COLOR_RGB2BGR,window_title='network')
		img_left_previous = img_left
		img_right_previous = img_right
		clf();xylim(0,7,0,8)
		plot(1/solver.net.blobs['target_markers'].data[-1,:],'ro-')
		plot(1/solver.net.blobs['ip_markers'].data[-1,:],'go-')
		plot(solver.net.blobs['ip_cars'].data[-1,:],'bo-')
		if k == ord('q'):
			break

	else:
		cars[our_car]['state_info']['pts'] = []


	return D

"""
