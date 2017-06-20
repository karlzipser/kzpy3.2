from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis2 import *
from data.utils.general import car_colors
import arena.planner.Markers as Markers

def Constants():

	D = {}

	bair_car_data_location_list = [opjD('bair_car_data_new_28April2017'),
		'/Volumes/SSD_2TB/bair_car_data_new_28April2017']

	D['bair_car_data_location'] = False
	for b in bair_car_data_location_list:
		print b
		if len(gg(b)) > 0:
			D['bair_car_data_location'] = b
			print_stars();print('*')
			print('bair_car_data_location = '+D['bair_car_data_location'])
			print('*');print_stars()
			pause(1)
			break
	if D['bair_car_data_location'] == False:
		print('bair_car_data_location not found!!!!!!')
		assert(False)

	D['trajectory_data_location'] = opjD('N.pkl')

	assert_disk_locations([D['bair_car_data_location'],D['trajectory_data_location']])

	D['type'] = 'Constants'

	D['Purpose'] = d2s(inspect.stack()[0][3],':','Constant values of various types.')
	
	D['Marker_Radius'] = 180*2.54/100.0 #4*107/100.0

	D['sensor_angles'] = -arange(-45,46,9)

	D['view_angle'] = 45#35

	D['view_angles'] = -D['sensor_angles']#arange(-D['view_angle'],D['view_angle']+1,10)

	D['DISPLAY_LEFT'] = True

	D['GRAPHICS'] = True

	D['GRAPHICS2'] = True

	D['markers'] = Markers.Markers(Markers.markers_clockwise,D['Marker_Radius']) #   4*107/100.)

	D['Origin'] = int(2*1000/300.*300 / 5)

	D['Mult'] = 1000/300.*50 / 5

	D['car_colors'] = car_colors

	D['car_names'] = ['Mr_Black','Mr_Silver','Mr_Yellow','Mr_Orange','Mr_Blue']

	D['n_for_heading'] = 15

	return D

C = Constants()

