from kzpy3.utils2 import *

GPU = 1
BATCH_SIZE = 100
DISPLAY = True
VERBOSE = True
MODEL = 'SqueezeNet'#'SqueezeNet_Aruco1'
LOAD_ARUCO = False
BAIR_CAR_DATA_PATH = opjD('bair_car_data_Main_Dataset')
#bair_car_data_path = opjD('bair_car_data_new_28April2017')
RESUME = False
print(MODEL)
if RESUME:
    weights_file_path = opjD('xxx')
IGNORE = ['reject_run','left','out1_in2']#,'Smyth','racing','local','Tilden','campus']
REQUIRE_ONE = []
USE_STATES = [1,3,5,6,7]
N_FRAMES = 2
N_STEPS = 10

save_net_timer = Timer(60*10)
print_timer = Timer(5)
#other_cars_only = True
HIGH_LOW_HISTOGRAM_FIGURE_NAME = 'high low steer histograms'