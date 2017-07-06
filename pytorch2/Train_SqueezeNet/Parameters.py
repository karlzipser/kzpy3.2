if '__file__' not in locals():
    __file__ = 'Parameters.py'

from kzpy3.utils2 import *
cprint('****************** '+__file__+' ******************','yellow')

GPU = 0
BATCH_SIZE = 100
DISPLAY = True
VERBOSE = True
LOAD_ARUCO = False
BAIR_CAR_DATA_PATH = opjD('bair_car_data_Main_Dataset') #opjD('bair_car_data_new_28April2017')
RESUME = False

if RESUME:
    weights_file_path = opjD('xxx')
IGNORE = ['reject_run','left','out1_in2']#,'Smyth','racing','local','Tilden','campus']
REQUIRE_ONE = []
USE_STATES = [1,3,5,6,7]
N_FRAMES = 2
N_STEPS = 10
STRIDE = 3 # multiply by N Steps in order to have fixed number of steps reach further in time.
save_net_timer = Timer(60*30)
print_timer = Timer(5)
epoch_timer = Timer(5)
#other_cars_only = True
HIGH_LOW_HISTOGRAM_FIGURE_NAME = 'high low steer histograms'

EPOCH_FINISHED = 'EPOCH FINISHED'




