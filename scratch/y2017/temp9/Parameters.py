from Names import *
exec(identify_file_str)

P = {}
P[GPU] = 1
P[BATCH_SIZE] = 100
P[DISPLAY] = True
P[VERBOSE] = True
P[LOAD_ARUCO] = False
P[BAIR_CAR_DATA_PATH] = opjD('bdd_car_data_July2017_LCR')
P[RESUME] = False
if RESUME:
    P[weights_file_path] = most_recent_file_in_folder(opjD(),['save_file'],['infer'])
P[IGNORE] = ['reject_run','left','out1_in2']#,'Smyth','racing','local','Tilden','campus']
P[REQUIRE_ONE] = []
P[USE_STATES] = [1,3,5,6,7]
P[N_FRAMES] = 2
P[N_STEPS] = 10
P[STRIDE] = 3 # multiply by N Steps in order to have fixed number of steps reach further in time.
# STRIDE is not fully controlled here, there must be changes in _data_into_batch().
P[save_net_timer] = Timer(60*30)
P[print_timer] = Timer(15)
P[epoch_timer] = Timer(15)
P[save_file_name] = 'save_file_LCR_'



print "HERE!!!!!!!"
#EOF