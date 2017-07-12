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
    weights_file_path = most_recent_file_in_folder(opjD(),['save_file'],['infer'])
IGNORE = ['reject_run','left','out1_in2']#,'Smyth','racing','local','Tilden','campus']
REQUIRE_ONE = []
USE_STATES = [1,3,5,6,7]
N_FRAMES = 2
N_STEPS = 10
STRIDE = 3 # multiply by N Steps in order to have fixed number of steps reach further in time.
# STRIDE is not fully controlled here, there must be changes in _data_into_batch().
save_net_timer = Timer(60*30)
print_timer = Timer(15)
epoch_timer = Timer(15)





#EOF