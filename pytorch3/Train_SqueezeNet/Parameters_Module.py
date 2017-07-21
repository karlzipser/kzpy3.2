from Names_Module import *
exec(identify_file_str)

P = {}

P[GPU] = 0
P[BATCH_SIZE] = 512*2
P[DISPLAY] = True
P[VERBOSE] = True
P[LOAD_ARUCO] = False
P[BAIR_CAR_DATA_PATH] = opjD('bdd_car_data_July2017_LCR')
P[RESUME] = False
if RESUME:
    P[WEIGHTS_FILE_PATH] = most_recent_file_in_folder(opjD(),['save_file'],['infer'])
P[IGNORE] = [reject_run,left,out1_in2]#,'Smyth','racing','local','Tilden','campus']
P[REQUIRE_ONE] = []
P[USE_STATES] = [1,2,3]
P[N_FRAMES] = 2
P[N_STEPS] = 10
P[STRIDE] = 3
P[SAVE_FILE_NAME] = 'save_file_LCR_temp_'
P[save_net_timer] = Timer(60*30)
P[print_timer] = Timer(15)
P[epoch_timer] = Timer(15)

#G = {}


#

#EOF