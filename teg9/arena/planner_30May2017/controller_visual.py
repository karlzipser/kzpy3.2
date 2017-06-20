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

trajectory_data_location = opjD('N.pkl')

angles = -arange(-45,46,9)
view_angle = 30

DISPLAY_LEFT = True
GRAPHICS = True

markers = Markers.Markers(Markers.markers_clockwise,4*107/100.)
Origin = int(2*1000/300.*300 / 5)
Mult = 1000/300.*50 / 5
#
#######################################










import kzpy3.caf8.protos as protos
solver = protos.setup_solver(opjh('kzpy3/caf8/z2_color_aruco/solver.prototxt'))
solver.net.copy_from('/Users/karlzipser/caffe_models/z2_color_aruco_potential_May2017/z2_color_iter_6500000.caffemodel')
#solver.net.copy_from('/Users/karlzipser/caffe_models/z2_color/z2_color.caffemodel')
solver.net.blobs['metadata'].data[0,:,:,:] *= 0
solver.net.blobs['metadata'].data[0,3,:,:] = 1








	
"""

follow speed modulated by distance_to_other_car
speed/gradient modulated by heading and distance to wall to give ahead of time turning and also stopping. Consider sampling
different proportions of direct and play, for example.
furtive speed modulated by distance to its grove, higher toward middle, lower in groove
play speed higher in middle

need distance to other cars, heading relative to radius vector
√ tune system so 99 is in right place.


output:

steer / motor / gradient values / other cars in view? /
"""







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
    		pfield['Image']['plot_pts'](array(sp)+array(pts[-1,:]),'g')
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
	if GRAPHICS:
		figure(9);plot(potential_values,'bo-')
	d = 99.0/(1.0*len(potential_values)-1)
	steer_angles = np.floor(99-arange(0,100,d))
	p = min(pmax/0.8,1.0)
	steer = int((p*steer_angles[min_potential_index]+(1-p)*49.0))
	return steer








def summarize_N_cars(N):
	for car_name in N.keys():
		print(car_name)
		summarize_N_runs(N,car_name)

def summarize_N_runs(N,car_name):
	for run_name in N[car_name].keys():
		print(d2n('\t',run_name))
		summarize_N_other_trajectories(N,car_name,run_name)

def summarize_N_other_trajectories(N,car_name,run_name):
		for other_runs in N[car_name][run_name]['other_trajectories']:
			print(d2n('\t\t',other_runs))










		

#heading_prev = 0
#near_t_prev = 0
img_left_previous = False


if __name__ == "__main__":



	
	if 'N' not in locals():
		print("Loading trajectory data . . .")
		N = lo(trajectory_data_location)

	
	if 'the_arenas' not in locals():
	#	the_arena = Potential_Fields.Direct_Arena_Potential_Field(Origin,Mult,markers)
	#	mode = the_arena['type']
		print("Creating arenas . . .")
		the_arenas = [Potential_Fields.Direct_Arena_Potential_Field(Origin,Mult,markers),
			Potential_Fields.Play_Arena_Potential_Field(Origin,Mult,markers),
			Potential_Fields.Follow_Arena_Potential_Field(Origin,Mult,markers),
			Potential_Fields.Furtive_Arena_Potential_Field(Origin,Mult,markers)]

	
	#if 'INITALIZED' not in locals():
	INITALIZED = True
	cars = {}
	for car_name in ['Mr_Black','Mr_Silver','Mr_Yellow','Mr_Orange','Mr_Blue']:
		cars[car_name] =  Cars.Car(N,car_name,Origin,Mult,markers)
	#run_name = 'direct_rewrite_test_28Apr17_17h23m15s_Mr_Black'
	#our_car = Cars.car_name_from_run_name(run_name)
	#our_car = random.choice(N.keys())
	#run_name = random.choice(N[our_car].keys())

	for our_car in ['Mr_Blue','Mr_Black','Mr_Silver','Mr_Yellow','Mr_Orange']: #cars.keys():
		for run_name in cars[our_car]['runs'].keys():
			output_data = {}
			output_name = opjD(run_name+'.output_data.pkl')
			output_data[run_name] = {}
			if len(gg(output_name)) > 0:
				print(output_name+' exists, continuing.')
				#time.sleep(1)
				continue
			else:
				print("Working on: "+output_name)
				#time.sleep(1)
			try:

				print(d2n(our_car,'\n\t',run_name))
				summarize_N_other_trajectories(N,our_car,run_name)


				T0 = cars[our_car]['runs'][run_name]['trajectory']['ts'][0]
				Tn = cars[our_car]['runs'][run_name]['trajectory']['ts'][-1]
				loct = cars[our_car]['runs'][run_name]['list_of_other_car_trajectories']
				try:
					cars[our_car]['load_image_and_meta_data'](run_name,bair_car_data_location)
				except Exception as e:
					print("********** Exception *** cars[our_car]['load_image_and_meta_data'](run_name,bair_car_data_location) ********************")
					print(mode,our_car,run_name)
					print(e.message, e.args)



				for the_arena_ctr in range(len(the_arenas)):
					the_arena = the_arenas[the_arena_ctr]
					mode = the_arena['type']
					print('mode = '+mode)

					output_data[run_name][mode] = {}
					output_data[run_name][mode]['sample_points'] = []
					output_data[run_name][mode]['potential_values'] = []
					output_data[run_name][mode]['steer'] = []
					output_data[run_name][mode]['real_steer'] = []
					output_data[run_name][mode]['motor'] = []
					output_data[run_name][mode]['real_motor'] = []
					output_data[run_name][mode]['near_t'] = []
					output_data[run_name][mode]['near_i'] = []
					output_data[run_name][mode]['other_cars_in_view'] = False

					print_stars()
					for car_name in cars:
						cars[car_name]['rewind']()
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
						if the_arena_ctr in [0,3]:
							if cars[our_car]['state_info']['relative_heading'] < 60:
								the_arena = the_arenas[1]
								#print "switch to Play"
							else:
								the_arena = the_arenas[the_arena_ctr]
						#print((mode,the_arena_ctr,cars[our_car]['state_info']['relative_heading']))
						#
						################
						


						t_prev = t
						if timer.check():
							print(time_str('Pretty'))
							timer.reset()
						p = cars[our_car]['report_camera_positions'](run_name,t)
						other_cars_add_list = []
						other_cars_point_list = []
						other_cars_angle_distance_list = []
						if len(p) > 0:
							pix = the_arena['Image']['floats_to_pixels'](p)
							p = array(p)
							xy_our = 1* p
							our_heading = cars[our_car]['state_info']['heading']
							p_mod = p
							no_cars_in_view = True
							for l in loct:
								other_car_name = l[0]
								other_car_run_name = l[1]
								p = cars[other_car_name]['report_camera_positions'](other_car_run_name,t)
								if len(p) > 0:
									other_cars_point_list.append(p)#[0])
									if our_heading != None:
										#angle_to_other_car = angle_clockwise(our_heading, array(p[0])-xy_our[0])
										#print(d2s('p:',p,'xy_our:',xy_our))
										angle_to_other_car = angle_clockwise(our_heading, array(p)-xy_our)
										if angle_to_other_car > 360-view_angle:
											angle_to_other_car = angle_to_other_car-360
										#distance_to_other_car = length(p[0]-xy_our[0])
										distance_to_other_car = length(p-xy_our)
										
										
										if angle_to_other_car > -view_angle and angle_to_other_car < view_angle: 
											#print((other_car_name,int(angle_to_other_car),dp(distance_to_other_car,2)))
											#other_cars_add_list.append(p[0])
											other_cars_angle_distance_list.append([angle_to_other_car,distance_to_other_car])
											other_cars_add_list.append(p)
											no_cars_in_view = False
							if no_cars_in_view:
								pass#continue
							the_arena['other_cars'](other_cars_add_list,mode,xy_our)
							img = the_arena['Image']['img']
							width = shape(img)[0]
							origin = Origin
							if GRAPHICS:
								mi(img,1)
								the_arena['Image']['plot_pts'](other_cars_point_list,'b')
								the_arena['Image']['plot_pts'](xy_our,'r')
							if len(other_cars_add_list) > 0:
								other_cars_add_list = array(other_cars_add_list)
								#xy = other_cars_add_list*0
								#xy[:,0] = other_cars_add_list[:,1]
								#xy[:,1] = other_cars_add_list[:,0]
							pause(0.000001)
							if cars[our_car]['state_info']['heading'] != None:
								sample_points,potential_values = get_sample_points(array(cars[our_car]['state_info']['pts']),angles,the_arena,cars[our_car]['state_info']['heading'])
								if mode == 'Follow_Arena_Potential_Field':
									for ang,dist in other_cars_angle_distance_list:
										indx = find_index_of_closest(-ang,angles)
										if dist > 1:
											potential_values[indx] *= (dist-1)/8.0
								steer = interpret_potential_values(potential_values)
								real_steer = cars[our_car]['runs'][run_name]['trajectory']['data']['steer'][cars[our_car]['state_info']['near_i']]

								output_data[run_name][mode]['sample_points'].append(sample_points)
								output_data[run_name][mode]['potential_values'].append(potential_values)
								output_data[run_name][mode]['steer'].append(steer)
								output_data[run_name][mode]['real_steer'].append(real_steer)
								output_data[run_name][mode]['near_t'].append(cars[our_car]['state_info']['near_t'])
								output_data[run_name][mode]['near_i'].append(cars[our_car]['state_info']['near_i'])
								"""
								heading = cars[our_car]['state_info']['heading']
								near_t = cars[our_car]['state_info']['near_t']
								if near_t - near_t_prev < 0.1:
									dheading = heading - heading_prev
									if np.degrees(angle_between(heading,heading_prev)) > 45:
										print_stars()
										print('Heading warning!!!')
										print_stars()
										heading = heading_prev
										#heading_warning_lst.append()
								else:
									dheading = None

								heading_prev = heading
								near_t_prev = near_t
								"""
								#figure('heading',figsize=(3,3));clf();xylim(-2,2,-2,2);#;raw_input('here!')
								#plot([0,heading[1]],[0,heading[0]],'r')
								#plot([0,heading[1]],[0,-heading[0]],'g');pause(0.01)
								

								#plot([0,-heading[1]],[0,heading[0]],'b')
								if GRAPHICS:
									figure(9)
									if ctr_q > 1:
										clf()
										ctr_q = 0
									plot(potential_values,'r.-');xylim(0,10,0,1);
									ctr_q += 1
									img_left = cars[our_car]['get_left_image'](run_name)
									img_right = cars[our_car]['get_right_image'](run_name)
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
									k = animate.prepare_and_show_or_return_frame(img=img,steer=steer,motor=None,state=6,delay=1,scale=2,color_mode=cv2.COLOR_RGB2BGR,window_title='network')
									img_left_previous = img_left
									img_right_previous = img_right
									#img = cars[our_car]['get_left_image'](run_name).copy()
									#k = animate.prepare_and_show_or_return_frame(img=img,steer=real_steer,motor=None,state=6,delay=1,scale=2,color_mode=cv2.COLOR_RGB2BGR,window_title='real')
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


def replay_potential_values(pv):
	ctr = 0
	for p in pv:
		if ctr >= 30:
			clf()
			ctr = 0
		plot(p,'r.-');xylim(0,9,0,2);pause(0.01)
		ctr += 1



