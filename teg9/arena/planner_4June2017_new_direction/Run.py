from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis import *
import data.utils.animate as animate
import arena.planner.Markers as Markers
import arena.planner.Potential_Fields as Potential_Fields
import arena.planner.Cars as Cars



	def _setup(run_name)

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



				the_arena = the_arenas[the_arena_type]
				mode = the_arena['type']
				print('mode = '+mode)







				for car_name in cars:
					cars[car_name]['rewind']()

				timer = Timer(10)
				stats=[]
				ctr_q = 0
				t_prev = 0





				for t in arange(T0,Tn,1/30.):
					
					

					
					t_prev = t
					if timer.check():
						print(time_str('Pretty'))
						timer.reset()


					spatial_configuration['compute'][t]







						if no_cars_in_view:
							pass#continue

						the_arena['other_cars'](other_cars_in_view_xy_list,mode,xy_our)
						img = the_arena['Image']['img']
						width = shape(img)[0]
						origin = Origin

						if GRAPHICS:
							mi(img,1)
							the_arena['Image']['plot_pts'](markers_in_view_xy_list,'c')
							the_arena['Image']['plot_pts'](other_cars_xy_list,'b')
							the_arena['Image']['plot_pts'](xy_our,'r')
							pause(0.000001)

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
								
								if ctr_q > 3:
									figure(9)
									clf()
									figure(10)
									clf()
									ctr_q = 0
								ctr_q += 1
								figure(9)
								plot(potential_values,'r.-');xylim(0,10,0,1);
								n=objects_to_angle_distance_representation(view_angles,other_cars_in_view_angle_distance_list)
								m=objects_to_angle_distance_representation(view_angles,markers_angle_distance_list)
								figure(10)
								plot(n,'r.-')
								plot(m,'b.-')
								pause(0.0001)
								
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



def Output_Data():
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
