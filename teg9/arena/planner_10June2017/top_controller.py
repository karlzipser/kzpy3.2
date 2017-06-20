from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis2 import *
import data.utils.animate as animate
from arena.planner.Constants import C
import arena.planner.Potential_Fields as Potential_Fields
import arena.planner.Cars as Cars
import arena.planner.Runs as Runs
import arena.planner.Spatial_Relations as Spatial_Relations


if 'N' not in locals():
	print("Loading trajectory data . . .")
	N = lo(C['trajectory_data_location'])

if 'the_arenas_ready' not in locals():
	print("Creating arenas . . .")
	args = []
	arenas_tmp_lst = [Potential_Fields.Follow_Arena_Potential_Field,
		Potential_Fields.Direct_Arena_Potential_Field,
		Potential_Fields.Play_Arena_Potential_Field,
		Potential_Fields.Furtive_Arena_Potential_Field]
	the_arenas = {}
	for a in arenas_tmp_lst:
		an_arena = a(C['Origin'],C['Mult'],C['markers'],False,1.0,1.5)
		the_arenas[an_arena['type']] = an_arena
		#break
	the_arenas_ready = True
	#img = an_arena['Image']['img'] #!!!!!!!!!! TEMP
	#img[img>1] = 0



cars = {}
for car_name in C['car_names']:
	cars[car_name] =  Cars.Car(N,car_name,C['Origin'],C['Mult'],C['markers'])


# cars['Mr_Yellow']['runs']['direct_rewrite_test_29Apr17_00h23m07s_Mr_Yellow']['trajectory']['data']['t_to_indx']

#current_run = Runs.Run('direct_rewrite_test_25Apr17_16h09m24s_Mr_Black',cars,an_arena,C['bair_car_data_location'])
current_run = Runs.Run('direct_rewrite_test_29Apr17_00h23m07s_Mr_Yellow',cars,an_arena,C['bair_car_data_location'])

# clockwise = 270° relative angle, to wall = 0°, counter-clockwise = 90°

for k in the_arenas:
	an_arena = the_arenas[k]

	T_OFFSET_VALUE = 0

	ctr_timer = Timer(0)
	timer = Timer(5)
	ctr = 0
	wise_delta = 10
	current_run['rewind']()
	clockwise = True
	for t in arange(current_run['T0']+T_OFFSET_VALUE,current_run['Tn'],1/30.):
		if timer.check():
			pd2s(dp(ctr/ctr_timer.time()/30.0),dp(t-current_run['T0']),dp(100.0*(t-current_run['T0'])/(current_run['Tn']-current_run['T0'])),'%')
			timer.reset()
		if Spatial_Relations.update_spatial_dics(current_run,current_run['car_spatial_dic'],current_run['marker_spatial_dic'],t):
			heading = current_run['our_car']['state_info']['heading']
			if heading != None:
				car_angle_dist_view = Spatial_Relations.get_angle_distance_view(current_run,'car_spatial_dic')

				if True:#len(car_angle_dist_view) > 0:

					other_cars_in_view_xy_list = []
					for c in current_run['car_spatial_dic'].keys():
						if current_run['car_spatial_dic'][c]['in_view']:
							other_cars_in_view_xy_list.append(current_run['car_spatial_dic'][c]['xy'])


					an_arena['other_cars'](other_cars_in_view_xy_list,an_arena['type'],current_run['our_car']['state_info']['pts'][-1])
					
					marker_angle_dist_view = Spatial_Relations.get_angle_distance_view(current_run,'marker_spatial_dic',are_markers=True)
					Runs.show_arena_with_cars(current_run,an_arena,t)
					pause(0.0001)
					potential_values = Spatial_Relations.get_sample_points(current_run['our_car']['state_info']['pts'],
						C['sensor_angles'],an_arena,heading)
					
					if an_arena['type'] == 'Follow_Arena_Potential_Field':
						dists = []
						for i in range(len(car_angle_dist_view)):
							inv_dist = car_angle_dist_view[i]
							dist = 1/(0.00001+inv_dist)
							dists.append(dist)
						if len(dists) > 0:
							if min(dists) <= 1:
								#print "A"
								pass
							else:
								for i in range(len(dists)):
									dist = dists[i]
									if dist >= 1 and dist < 8:
										potential_values[i] *= 1.0/(9.0-dist)
					else:
						potential_values = 3*array(potential_values)
					relative_heading = current_run['our_car']['state_info']['relative_heading']
					if relative_heading > 360-wise_delta or relative_heading <= wise_delta:
						direction = 'in'
					elif relative_heading > wise_delta and relative_heading <= 180-wise_delta:
						direction = 'counter-clockwise'
					elif relative_heading > 180+wise_delta and relative_heading <= 360-wise_delta:
						direction = 'clockwise'
					else:
						direction = 'out'
					if direction == 'clockwise':
						if not clockwise:
							clockwise = True
					elif direction == 'counter-clockwise':
						if clockwise:
							clockwise = False
					#pd2s(dp(relative_heading),direction,'clockwise =',clockwise)

					clock_potential_values = z2o(arange(len(potential_values)))
					if clockwise:
						clock_potential_values = 1 - clock_potential_values
					clock_potential_values *= 5.0*length(0.5+current_run['our_car']['state_info']['pts'][-1])/C['Marker_Radius']

					if relative_heading >= 0 and relative_heading < 90:
						clock_potential_values *= abs(95-relative_heading)/90.0
					elif relative_heading >= 270 and relative_heading <= 360:
						clock_potential_values *= abs(relative_heading-265)/90.0
					else:
						clock_potential_values *= 0

					ctr += 1
					figure('view')
					clf()
					xylim(0,11,0,5)
					plot(car_angle_dist_view,'r.-')
					plot(marker_angle_dist_view,'b.-')
					plot(potential_values,'rx-')
					plot(clock_potential_values,'gx-')
					plot(potential_values+clock_potential_values,'ko-')
					print Spatial_Relations.interpret_potential_values(list(potential_values+clock_potential_values))
					mci(current_run['our_car']['get_image'](current_run['run_name'],'right'),title='right',scale=2.0)
		else:
			continue
			#clf()
			#current_run['the_arena']['show']()
			#pause(0.0001)
		if ctr_timer.time() > 60:
			break
				