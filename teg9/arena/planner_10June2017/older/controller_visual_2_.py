from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis import *
import data.utils.animate as animate
import arena.planner.Markers as Markers
import arena.planner.Potential_Fields as Potential_Fields
import arena.planner.Cars as Cars

#######################################
#
#bair_car_data_location = '/media/karlzipser/bair_car_data_new_bkp1/bair_car_data_new_28April2017'
#bair_car_data_location = '/media/karlzipser/SSD_2TB/bair_car_data_new_28April2017'
bair_car_data_location = '/Volumes/SSD_2TB/bair_car_data_new_28April2017'
#bair_car_data_location = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'
#bair_car_data_location = opjD('bair_car_data_new_28April2017')

trajectory_data_location = opjD('N.pkl')
for p in [bair_car_data_location,trajectory_data_location]:
	assert(len(gg(p))) > 0
#
#######################################
#
angles = -arange(-45,46,9)
view_angle = 35
view_angles = arange(-view_angle,view_angle+1,10)

DISPLAY_LEFT = True
GRAPHICS = True
markers = Markers.Markers(Markers.markers_clockwise,4*107/100.)
Origin = int(2*1000/300.*300 / 5)
Mult = 1000/300.*50 / 5
#
#######################################

##############################
#
if 'N' not in locals():
	print("Loading trajectory data . . .")
	N = lo(trajectory_data_location)

if 'the_arenas' not in locals():
	print("Creating arenas . . .")
	arenas_tmp_lst = [Potential_Fields.Direct_Arena_Potential_Field(Origin,Mult,markers),
		Potential_Fields.Play_Arena_Potential_Field(Origin,Mult,markers),
		Potential_Fields.Follow_Arena_Potential_Field(Origin,Mult,markers),
		Potential_Fields.Furtive_Arena_Potential_Field(Origin,Mult,markers)]
	the_arenas = {}
	for a in arenas_tmp_lst:
		the_arenas[a['type']] = a

cars = {}
for car_name in ['Mr_Black','Mr_Silver','Mr_Yellow','Mr_Orange','Mr_Blue']:
	cars[car_name] =  Cars.Car(N,car_name,Origin,Mult,markers)
#
###############################

#######################################
#
USE_CAFFE = True
if USE_CAFFE:
	import caf8.protos as protos
	solver = protos.setup_solver(opjh('kzpy3/caf8/z2_color_aruco/solver.prototxt'))
	solver.net.copy_from('/Users/karlzipser/Desktop/z2_color_aruco_iter_400000.caffemodel')
	#solver.net.copy_from('/Users/karlzipser/caffe_models/z2_color/z2_color.caffemodel')
	img_left_previous = False
#
#######################################








def get_sample_points(pts,angles,pfield,heading):
    sample_points = []
    potential_values = []
    heading *= 0.5 # 50 cm, about the length of the car
    for the_arena in angles:
        sample_points.append( rotatePoint([0,0],heading,the_arena) )
    for k in range(len(sample_points)):
        f = sample_points[k]
    for sp in sample_points:
    	if GRAPHICS:
    		pass#pfield['Image']['plot_pts'](array(sp)+array(pts[-1,:]),'g')
        pix = pfield['Image']['floats_to_pixels']([sp[0]+pts[-1,0],sp[1]+pts[-1,1]])
        potential_values.append(pfield['Image']['img'][pix[0],pix[1]])
    return sample_points,potential_values

def interpret_potential_values(potential_values):
	min_potential_index = potential_values.index(min(potential_values))
	max_potential_index = potential_values.index(max(potential_values))
	middle_index = int(len(potential_values)/2)
	potential_values = array(potential_values)
	pmin = potential_values.min()
	pmax = potential_values.max()
	potential_values = z2o(potential_values) * pmax
	#if GRAPHICS:
	#	figure(9);plot(potential_values,'bo-')
	d = 99.0/(1.0*len(potential_values)-1)
	steer_angles = np.floor(99-arange(0,100,d))
	p = min(pmax/0.8,1.0)
	steer = int((p*steer_angles[min_potential_index]+(1-p)*49.0))
	return steer


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






for our_car in ['Mr_Black','Mr_Silver','Mr_Yellow','Mr_Orange','Mr_Blue']:

	for run_name in cars[our_car]['runs'].keys():
		if len(gg(opjD(bair_car_data_location,'meta',run_name,'*'))) < 5: #'caffe2_z2_color_direct_local_01Jan13_00h01m07s_Mr_Yellow' in run_name:
			print("len(gg(opjD(bair_car_data_location,'meta',run_name,'*'))) < 5")
			continue
		velocity = (cars[our_car]['runs'][run_name]['trajectory']['left']['t_vel']+cars[our_car]['runs'][run_name]['trajectory']['right']['t_vel'])/2.0
		#velocity = mean_exclude_outliers(velocity,15,1/3.0,2/3.0)
		output_data = {}

		output_name = opjD('output_data',run_name+'.output_data.pkl')

		output_data[run_name] = {}

		if len(gg(output_name)) > 0:
			print(output_name+' exists, continuing.')
			continue
		else:
			print(output_name+" does not exist, processing it now.")

		for the_arena_type in ['Direct_Arena_Potential_Field']:
			the_arena = the_arenas[the_arena_type]
			mode = the_arena['type']
			print('mode = '+mode)

			try:

				print(d2n(our_car,'\n\t',run_name))
				zaccess(N[our_car][run_name],[0]);

				T0 = cars[our_car]['runs'][run_name]['trajectory']['ts'][0]
				Tn = cars[our_car]['runs'][run_name]['trajectory']['ts'][-1]
				list_of_other_car_trajectories = cars[our_car]['runs'][run_name]['list_of_other_car_trajectories']
				try:
					cars[our_car]['load_image_and_meta_data'](run_name,bair_car_data_location)
				except Exception as e:
					print("********** Exception *** cars[our_car]['load_image_and_meta_data'](run_name,bair_car_data_location) ********************")
					print(our_car,run_name)
					print(e.message, e.args)

				if USE_CAFFE:
					solver.net.blobs['metadata'].data[0,:,:,:] *= 0
					if mode == 'Direct_Arena_Potential_Field':
						solver.net.blobs['metadata'].data[0,3,:,:] = 1
					elif mode == 'Furtive_Arena_Potential_Field':
						solver.net.blobs['metadata'].data[0,5,:,:] = 1
					elif mode == 'Follow_Arena_Potential_Field':
						solver.net.blobs['metadata'].data[0,2,:,:] = 1
					elif mode == 'Play_Arena_Potential_Field':
						solver.net.blobs['metadata'].data[0,4,:,:] = 1
					else:
						CS_("Unknown mode!")
						assert(False)

				output_data[run_name][mode] = {}
				output_data[run_name][mode]['sample_points'] = []
				output_data[run_name][mode]['potential_values'] = []
				output_data[run_name][mode]['steer'] = []
				output_data[run_name][mode]['real_steer'] = []
				output_data[run_name][mode]['motor'] = []
				output_data[run_name][mode]['real_motor'] = []
				output_data[run_name][mode]['near_t'] = []
				output_data[run_name][mode]['near_i'] = []
				output_data[run_name][mode]['other_cars_in_view'] = []
				output_data[run_name][mode]['other_car_inverse_distances'] = []
				output_data[run_name][mode]['marker_inverse_distances'] = []
				output_data[run_name][mode]['velocity'] = []

				print_stars(2)

				if GRAPHICS:			
					plt.figure(1,figsize=(4,4));clf();ds = 5;xylim(-ds,ds,-ds,ds)

				for car_name in cars:
					cars[car_name]['rewind']()

				timer = Timer(10)
				stats=[]
				ctr_q = 0
				t_prev = 0





				for t in arange(T0+210,Tn,1/30.):
					
					
					################
					#
					"""
					if mode in ['Direct_Arena_Potential_Field','Furtive_Arena_Potential_Field']:
						if cars[our_car]['state_info']['relative_heading'] < 60:
							the_arena = the_arenas['Play_Arena_Potential_Field']
							#print "switch to Play"
						else:
							the_arena = the_arenas[mode]
					#	print((mode,the_arena_ctr,cars[our_car]['state_info']['relative_heading']))
					"""
					#
					################
					
					t_prev = t
					if timer.check():
						print(time_str('Pretty'))
						timer.reset()


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



									"""
									angle_to_other_car = angle_clockwise(our_heading, array(xy_other)-xy_our)
									if angle_to_other_car > 360-view_angle:
										angle_to_other_car = angle_to_other_car-360
									distance_to_other_car = length(xy_other-xy_our)
									
									if angle_to_other_car > -view_angle and angle_to_other_car < view_angle: 
										other_cars_angle_distance_list.append([angle_to_other_car,distance_to_other_car])
										other_cars_in_view_xy_list.append(xy_other)
										no_cars_in_view = False
									"""




						if no_cars_in_view:
							if np.random.random() < 0.25:
								continue

						the_arena['other_cars'](other_cars_in_view_xy_list,mode,xy_our)
						img = the_arena['Image']['img']
						width = shape(img)[0]
						origin = Origin

						if GRAPHICS:
							"""
							mi(img,1)
							the_arena['Image']['plot_pts'](markers_in_view_xy_list,'c')
							the_arena['Image']['plot_pts'](other_cars_xy_list,'b')
							the_arena['Image']['plot_pts'](xy_our,'r')
							pause(0.000001)
							"""
						#if len(other_cars_in_view_xy_list) > 0:
						#	other_cars_in_view_xy_list = array(other_cars_in_view_xy_list)
						if cars[our_car]['state_info']['heading'] != None:
							sample_points,potential_values = get_sample_points(array(cars[our_car]['state_info']['pts']),angles,the_arena,cars[our_car]['state_info']['heading'])
							if mode == 'Follow_Arena_Potential_Field':
								for ang,dist in other_cars_angle_distance_list:
									indx = find_index_of_closest(-ang,angles)
									if dist > 1:
										potential_values[indx] *= (dist-1)/8.0
							steer = interpret_potential_values(potential_values)
							real_steer = cars[our_car]['runs'][run_name]['trajectory']['data']['steer'][cars[our_car]['state_info']['near_i']]
							vel = velocity[cars[our_car]['state_info']['near_i']]
							n=objects_to_angle_distance_representation(view_angles,other_cars_in_view_angle_distance_list)
							m=objects_to_angle_distance_representation(view_angles,markers_angle_distance_list)
							output_data[run_name][mode]['sample_points'].append(sample_points)
							output_data[run_name][mode]['potential_values'].append(potential_values)
							output_data[run_name][mode]['steer'].append(steer)
							output_data[run_name][mode]['real_steer'].append(real_steer)
							output_data[run_name][mode]['near_t'].append(cars[our_car]['state_info']['near_t'])
							output_data[run_name][mode]['near_i'].append(cars[our_car]['state_info']['near_i'])
							output_data[run_name][mode]['velocity'].append(vel)
							output_data[run_name][mode]['other_car_inverse_distances'].append(n)
							output_data[run_name][mode]['marker_inverse_distances'].append(m)
							if GRAPHICS:
								"""
								if ctr_q > 3:
									figure(9)
									clf()
									figure(10)
									clf()
									ctr_q = 0
								ctr_q += 1
								"""
								#figure(9)
								#plot(potential_values,'r.-');xylim(0,10,0,1);
								n=objects_to_angle_distance_representation(view_angles,other_cars_in_view_angle_distance_list)
								m=objects_to_angle_distance_representation(view_angles,markers_angle_distance_list)
								figure(10)
								#plot(n,'r.-')
								#plot(m,'b.-')
								pause(0.0001)
								
								img_left = cars[our_car]['get_image'](run_name,'left')
								img_right = cars[our_car]['get_image'](run_name,'right')
								img = img_left.copy()
								#k = animate.prepare_and_show_or_return_frame(img=img,steer=steer,motor=None,state=1,delay=1,scale=2,color_mode=cv2.COLOR_RGB2BGR,window_title='plan')
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

									#print(solver.net.blobs['ip_cars'].data[-1,:])
									clf();xylim(0,7,0,2);plot(4*solver.net.blobs['ip_cars'].data[-1,:],'b-')
									plot(solver.net.blobs['ip_markers'].data[-1,:],'ro-')
									plot(solver.net.blobs['target_markers'].data[-1,:],'bo-')
									"""
									for plot_data in [
										['target_markers','ip_markers']]:#,['target_cars','ip_cars'],]:
										clf();#figure(plot_data[0]);clf()
										t = solver.net.blobs[plot_data[0]].data[-1,:]
										o = solver.net.blobs[plot_data[1]].data[-1,:]
										lim(-0.05,2.05);xlim(-0.5,len(t)-0.5)
										plot([-1,60],[0.49,0.49],'k');plot(o,'og'); plot(t,'or'); plt.title(data['name'])
									pause(0.001)
									"""

								img = img_left.copy()
								k = animate.prepare_and_show_or_return_frame(img=img,steer=steer,motor=20.0*vel+49,state=6,delay=1,scale=2,color_mode=cv2.COLOR_RGB2BGR,window_title='network')
								img_left_previous = img_left
								img_right_previous = img_right
								if k == ord('q'):
									break

					else:
						cars[our_car]['state_info']['pts'] = []
			except Exception as e:
				print("********** Exception ***********************")
				print(our_car,run_name)
				print(e.message, e.args)						

		so(output_data,output_name)
		print('saved '+output_name)
		print(output_data[run_name].keys())
		print_stars()


