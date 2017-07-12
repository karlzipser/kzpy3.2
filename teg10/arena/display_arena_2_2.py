from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])

from vis import *
import data.utils.general
from data.utils.general import car_name_from_run_name
from data.utils.general import car_colors as colors
import arena.arena_display as arena_display
from arena.objects import Markers
from arena.markers_clockwise import markers_clockwise

DISPLAY_LEFT = True
#bair_car_data_location = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'
bair_car_data_location = '/Volumes/SSD_2TB/bair_car_data_new_28April2017'
markers = Markers(markers_clockwise,4*107/100.)
if 'N' not in locals():
	print("Loading trajectory data . . .")
	N = lo(opjD('N_pruned.pkl'))


"""
for car_name in N.keys():
	for run_name in N[car_name].keys():
		for i in range(len(N[car_name][run_name]['other_trajectories'])):
			del N[car_name][run_name]['other_trajectories'][i]['left']
			del N[car_name][run_name]['other_trajectories'][i]['right']
			del N[car_name][run_name]['other_trajectories'][i]['camera_separation']
			del N[car_name][run_name]['other_trajectories'][i]['ts']
so(N,opjD('N_pruned'))
"""


while True:

	CAR_NAME = random.choice(N.keys())
	RUN_NAME = random.choice(N[CAR_NAME].keys())
	if len(N[CAR_NAME][RUN_NAME]['other_trajectories']) > 1:
		break

arena_display.display_arena(N,CAR_NAME,RUN_NAME,markers,bair_car_data_location,DISPLAY_LEFT)







