from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis2 import *
import data.utils.animate as animate
import arena.planner.Potential_Fields as Potential_Fields
reload(Potential_Fields)
import arena.planner.Cars as Cars
reload(Cars)
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
	if len(gg(opjD(bair_car_data_location,'meta',run_name,'*'))) < 5:
			print_stars()
			print("len(gg(opjD(bair_car_data_location,'meta',run_name,'*'))) < 5")
			print_stars()
			return False
	traj = our_car['runs'][run_name]['traj']
	D['T0'] = traj['ts'][0]
	D['Tn'] = traj['ts'][-1]
	D['list_of_other_car_trajectories'] = our_car['runs'][run_name]['list_of_other_car_trajectories']
	def _rewind():
		for c in C['car_names']:
			D['cars'][c]['rewind']()
	D['rewind'] = _rewind
	car_spatial_dic,marker_spatial_dic = Spatial_Relations.setup_spatial_dics(D)
	D['car_spatial_dic'] = car_spatial_dic
	D['marker_spatial_dic'] = marker_spatial_dic
	D['rewind']()
	return D


def show_arena_with_cars(current_run,an_arena,t):
	car_spatial_dic,marker_spatial_dic = current_run['car_spatial_dic'],current_run['marker_spatial_dic']
	if len(current_run['our_car']['current_xy']()) > 0:
		xy = current_run['our_car']['current_xy']()
		an_arena['show']()
		an_arena['Image']['pts_plot'](xy,'r')
		heading = current_run['our_car']['current_heading']()
		
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


