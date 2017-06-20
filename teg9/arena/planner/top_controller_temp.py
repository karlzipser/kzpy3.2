from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis2 import *
import data.utils.animate as animate
from arena.planner.Constants import C
import arena.planner.Potential_Fields as Potential_Fields
import arena.planner.Cars as Cars
import arena.planner.Runs as Runs
import arena.planner.Spatial_Relations as Spatial_Relations
import data.utils.general
# clockwise = 270 relative angle, to wall = 0, counter-clockwise = 90

# Add potential measures and relative heading value




PROCESS_NUM = 0#= int(sys.argv[1])

pd2s('PROCESS_NUM =',PROCESS_NUM)

def Processes():
	D = {}
	D['processes'] = []
	ctr = 0
	for car_name in C['car_names']:
		for desired_direction in ['clockwise','counter-clockwise']:
			D['processes'].append((car_name,desired_direction))
	return D
processes = Processes()

run_values_dic = {}
run_values_dic['GRAPHICS'] = True
run_values_dic['SAVE_DATA'] = False
run_values_dic['T_OFFSET_VALUE'] = 0
run_values_dic['TIME_STEP'] = 1/30.0
run_values_dic['desired_direction'] = d2n("""\'""",processes['processes'][PROCESS_NUM][1],"""\'""")
run_values_dic['current_car_name'] = d2n("""\'""",processes['processes'][PROCESS_NUM][0],"""\'""")

print_stars();print('*')
for k in sorted(run_values_dic.keys()):
    print(k+' = '+str(run_values_dic[k]))
    exec(k+' = '+str(run_values_dic[k]))
print('*');print_stars()




img_ctr = 0


if GRAPHICS:
	PAUSE = False

if 'N' not in locals():
	print("Loading trajectory data . . .")
	N = lo(C['trajectory_data_location'])

if True: #len(gg(opjD('the_arenas.pkl'))) == 0:
	if 'the_arenas_ready' not in locals():
		print("Creating arenas . . .")
		arenas_tmp_lst = [Potential_Fields.Direct_Arena_Potential_Field]#,Potential_Fields.Follow_Arena_Potential_Field]#,
		#Potential_Fields.Play_Arena_Potential_Field,
		#Potential_Fields.Furtive_Arena_Potential_Field]
		the_arenas = {}
		for a in arenas_tmp_lst:
			an_arena = a(C['Origin'],C['Mult'],C['markers'],False,1.0,1.5)
			the_arenas[an_arena['type']] = an_arena
		del arenas_tmp_lst
		the_arenas_ready = True

	#so(opjD('the_arenas'),the_arenas)
else:
	pass
	#the_arenas = lo(opjD('the_arenas'))

if 'the_cars_ready' not in locals():
	print("Loading cars . . .")
	cars = {}
	for car_name in C['car_names']:
		cars[car_name] =  Cars.Car(N,car_name,C['Origin'],C['Mult'],C['markers'],C['bair_car_data_location'])
	the_cars_ready = True

if SAVE_DATA:
	unix('mkdir -p '+opjD('output_data'))

car_name = current_car_name
#for car_name in [C['car_names'][0]]:

for run_name in cars[car_name]['runs'].keys():
	output_data = {}
	try:

		current_run = Runs.Run(run_name,cars,an_arena,C['bair_car_data_location'])
		current_run['rewind']()
		if GRAPHICS:
			images = data.utils.general.get_bag_pkl_images(current_run['run_name'],C['bair_car_data_location'])

		output_data[run_name] = {}
		output_name = opjD('output_data',run_name+'.'+desired_direction+'.pkl')

		if SAVE_DATA:
			if len(gg(output_name)) > 0:
				print(output_name+' exists, continuing.')
				continue

		for k in the_arenas:

			an_arena = the_arenas[k]
			mode = an_arena['type']
			output_data[run_name][mode] = {}
			output_data[run_name][mode]['potential_values'] = []
			output_data[run_name][mode]['steer'] = []
			output_data[run_name][mode]['velocity'] = []
			output_data[run_name][mode]['near_t'] = []
			output_data[run_name][mode]['near_i'] = []
			output_data[run_name][mode]['marker_inverse_distances'] = []
			output_data[run_name][mode]['other_car_inverse_distances'] = []
			output_data[run_name][mode]['relative_heading'] = []
			output_data[run_name][mode]['desired_direction'] = []
			output_data[run_name][mode]['clock_potential_values'] = []

			relative_heading_prev = 0

			ctr_timer = Timer(0)
			timer = Timer(5)
			pause_timer = Timer(60)
			ctr = 0
			wise_delta = 10
			current_run['rewind']()


			t = current_run['T0']+T_OFFSET_VALUE
			while t <= current_run['Tn']:
				if GRAPHICS and pause_timer.check():
					ri = raw_input('hit enter to continue, or cc or cw: ')
					if ri == "cc":
						desired_direction = "counter-clockwise"
					elif ri == "cw":
						desired_direction = "clockwise"
					pause_timer.reset()
				if timer.check():
					pd2s(dp(ctr/ctr_timer.time()/30.0),'Hz',dp(t-current_run['T0']),'seconds in',dp(100.0*(t-current_run['T0'])/(current_run['Tn']-current_run['T0'])),'%')
					timer.reset()
				if Spatial_Relations.update_spatial_dics(current_run,current_run['car_spatial_dic'],current_run['marker_spatial_dic'],t):
					heading = current_run['our_car']['current_heading']()
					if heading != None:
						car_angle_dist_view = Spatial_Relations.get_angle_distance_view(current_run,'car_spatial_dic')

						##################
						#
						if len(car_angle_dist_view) > 0 and current_run['our_car']['current_velocity']()>0.6:
						#
						##################
						
							other_cars_in_view_xy_list = []
							for c in current_run['car_spatial_dic'].keys():
								if current_run['car_spatial_dic'][c]['in_view']:
									other_cars_in_view_xy_list.append(current_run['car_spatial_dic'][c]['xy'])


							an_arena['other_cars'](other_cars_in_view_xy_list,an_arena['type'],current_run['our_car']['current_xy']())
							
							marker_angle_dist_view = Spatial_Relations.get_angle_distance_view(current_run,'marker_spatial_dic',are_markers=True)
							
							potential_values = Spatial_Relations.get_sample_points(current_run['our_car']['current_xy'](),
								C['sensor_angles'],an_arena,heading)
							
							if an_arena['type'] == 'Follow_Arena_Potential_Field':
								dists = []
								for i in range(len(car_angle_dist_view)):
									inv_dist = car_angle_dist_view[i]
									dist = 1/(0.00001+inv_dist)
									dists.append(dist)
								if len(dists) > 0:
									if min(dists) <= 1:
										pass
									else:
										for i in range(len(dists)):
											dist = dists[i]
											if dist >= 1 and dist < 8:
												potential_values[i] *= 1.0/(9.0-dist)
							else:
								potential_values = 3*array(potential_values)


							
							relative_heading = current_run['our_car']['current_relative_heading']()
							direction = current_run['our_car']['current_direction']()
							
		

							clock_potential_values = z2o(arange(len(potential_values)))

							direction_matches_desired = False

							if desired_direction == 'clockwise':
								if direction == 'clockwise':
									#t += TIME_STEP;continue
									clock_potential_values = 1 - clock_potential_values
									clock_potential_values *= 2.0*length(current_run['our_car']['current_xy']())/C['Marker_Radius']
									direction_matches_desired = True
								elif direction in ['counter-clockwise']:
									#t += TIME_STEP;continue
									pass
								elif direction in ['out']:
									#t += TIME_STEP;continue
									clock_potential_values *= 0.0
								elif direction in ['in']:
									#t += TIME_STEP;continue
									clock_potential_values = 1 - clock_potential_values
								else:
									assert(False)
							elif desired_direction == 'counter-clockwise':
								if direction == 'counter-clockwise':
									#t += TIME_STEP;continue
									clock_potential_values *= 2.0*length(current_run['our_car']['current_xy']())/C['Marker_Radius']
									direction_matches_desired = True
								elif direction in ['clockwise']:
									#t += TIME_STEP;continue
									clock_potential_values = 1 - clock_potential_values
								elif direction in ['in']:
									#t += TIME_STEP;continue
									pass
								elif direction in ['out']:
									#t += TIME_STEP;continue
									clock_potential_values *= 0.0
								else:
									assert(False)
							else:
								assert(False)



							if direction_matches_desired:
								if relative_heading >= 0 and relative_heading < 90:
									clock_potential_values *= abs(90-relative_heading)/90.0
								elif relative_heading >= 270 and relative_heading <= 360:
									clock_potential_values *= abs(relative_heading-270)/90.0
								else:
									clock_potential_values *= 0



							ctr += 1




							new_steer = Spatial_Relations.interpret_potential_values(list(potential_values+clock_potential_values))


							if GRAPHICS:
								print(desired_direction,direction,int(relative_heading),new_steer,int(t-current_run['T0']),dp(current_run['our_car']['current_velocity']()))


							output_data[run_name][mode]['marker_inverse_distances'].append(marker_angle_dist_view)
							output_data[run_name][mode]['other_car_inverse_distances'].append(car_angle_dist_view)
							output_data[run_name][mode]['potential_values'].append(potential_values)
							output_data[run_name][mode]['steer'].append(new_steer)
							output_data[run_name][mode]['near_t'].append(current_run['our_car']['near_t'])
							output_data[run_name][mode]['near_i'].append(current_run['our_car']['near_i'])
							output_data[run_name][mode]['velocity'].append(current_run['our_car']['current_velocity']())
							output_data[run_name][mode]['relative_heading'].append(relative_heading)
							output_data[run_name][mode]['clock_potential_values'].append(clock_potential_values)
							if desired_direction == 'clockwise':
								dd = 0
							else:
								dd = 1
							output_data[run_name][mode]['desired_direction'].append(dd)

							if GRAPHICS:
								if False:
									Runs.show_arena_with_cars(current_run,an_arena,t)
									figure('view')
									clf()
									xylim(0,10,0,2)
									plot(potential_values+clock_potential_values,'ko-')
									plot(car_angle_dist_view,'y.-')
									plot(marker_angle_dist_view,'b.-')
									plot(potential_values,'r.-')
									plot(clock_potential_values,'gx-')
									plt.title(d2s(new_steer))
									pause(0.0001)
								
								near_t = current_run['our_car']['near_t']
								img = images['left'][near_t]
								k = mci(img,delay=1,title='images',scale=2.0)
								imsave(opjD('cars',str(img_ctr)+'.png'),img)
								img_ctr += 1
								if k != -1:
									pd2s("k =",k)
									if not PAUSE:
										time_step = TIME_STEP
									if k == ord('q'):
										print('q')
										break
									if k == ord('d'):
										print('done')
										DONE = True
										cv2.destroyAllWindows()
										sys.exit()
									elif k == ord('k'):
										pd2s('t from',t)
										t -= 2
										pd2s('to',t)
									elif k == ord('l'):
										t += 2
									elif k == ord(' '):
										if PAUSE:
											PAUSE = False
											TIME_STEP = time_step
											print("<<end pause>>")
										else:
											PAUSE = True
											time_step = TIME_STEP
											TIME_STEP = 0
											print("<<pause>>")

					t += TIME_STEP
				else:
					t += TIME_STEP

					continue

				


		if SAVE_DATA:
			so(output_data,output_name)
			print('saved '+output_name)
			print(output_data[run_name].keys())
			print_stars()


	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
		print_stars()

print_stars1()
print("FINISHED")
print_stars2()