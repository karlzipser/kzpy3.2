#from All_Names_Module import *
from kzpy3.utils2 import *
exec(identify_file_str)

P = {}

P[GPU] = 0
P[BATCH_SIZE] = 64
P[DISPLAY] = True
P[VERBOSE] = True
P[LOAD_ARUCO] = False
P[BAIR_CAR_DATA_PATH] = opjD('bdd_car_data_July2017_LCR')
P[CODE_PATH] = opjD('LCR_temp/code')#CODE_PATH__
P[IGNORE] = [reject_run,left,out1_in2]#,'Smyth','racing','local','Tilden','campus']
P[REQUIRE_ONE] = []
P[USE_STATES] = [1,2,3]
P[N_FRAMES] = 2
P[N_STEPS] = 10
P[STRIDE] = 9#3 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
P[NETWORK_OUTPUT_FOLDER] = opjD('LCR_temp')
P[SAVE_FILE_NAME] = 'save_file_LCR_pt3'
P[save_net_timer] = Timer(60*30)
P[print_timer] = Timer(15)
P[TRAIN_TIME] = 60*10.0
P[VAL_TIME] = 60*1.0
P[RESUME] = True
if RESUME:
    P[INITIAL_WEIGHTS_FOLDER] = opj(P[NETWORK_OUTPUT_FOLDER],'weights')
    P[WEIGHTS_FILE_PATH] = most_recent_file_in_folder(P[INITIAL_WEIGHTS_FOLDER],['save_file'],[])



#

#EOF