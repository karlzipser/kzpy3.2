from kzpy3.utils2 import *

GPU = 0
BATCH_SIZE = 100
DISPLAY = False
MODEL = 'SqueezeNet_Aruco1'
RESUME = True
print(MODEL)
if RESUME:
    weights_file_path = opjD('save_file.weights')
ignore = ['reject_run','left','out1_in2']#,'Smyth','racing','local','Tilden','campus']
require_one = []
use_states = [1,3,5,6,7]
#bair_car_data_path = opjD('bair_car_data_Main_Dataset')
bair_car_data_path = opjD('bair_car_data_new_28April2017')
save_net_timer = Timer(60*10)


