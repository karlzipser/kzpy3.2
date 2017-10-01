
from Paths_Module import *
from utils2 import *

print 2,os.environ['PYTHONPATH'].split(os.pathsep)


# save loss records for train and val, times and moment numbers
# save loss by moment id
# save weights
# save other state variables
#current_code_dst_folder = opj(code,time_str())
#for folder in [code,current_code_dst_folder,loss_history,weights]:
#	unix('mkdir -p '+opj(P[NETWORK_OUTPUT_FOLDER],folder))
#unix('scp -r '+P[CODE_PATH]+' '+opj(P[NETWORK_OUTPUT_FOLDER],current_code_dst_folder))



from utils2 import *
exec(identify_file_str)


P = {}
#P['data_moments_indexed'] =  lo('/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/data_moments_indexed_1.pkl')

P[LOSS_TIMER] = Timer(60*5)
P[PRINT_TIMER] = Timer(1)
P[FREQUENCY_TIMER] = Timer(10.0)
P[LOSS_LIST] = []
P[LOSS_LIST_AVG] = []
P[GPU] = 1
P[BATCH_SIZE] = 1
P[DISPLAY] = True
P[VERBOSE] = True
P[LOAD_ARUCO] = False
P[BAIR_CAR_DATA_PATH] = opjD('bdd_car_data_Sept2017_aruco_demo')

P[IGNORE] = [reject_run,left,out1_in2]#,'Smyth','racing','local','Tilden','campus']
P[REQUIRE_ONE] = []
P[USE_STATES] = [1,3,5,6,7]
P[N_FRAMES] = 2
P[N_STEPS] = 10
P[N_OUTPUTS] = 20
P[STRIDE] = 1#9#3 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
P[NETWORK_OUTPUT_FOLDER] = opjD('IMU_net')
P[SAVE_FILE_NAME] = 'net'
P[SAVE_NET_TIMER] = Timer(60*5)

P[TRAIN_TIME] = 60*10.0
P[VAL_TIME] = 60*1.0
P[RESUME] = False
if RESUME:
    P[INITIAL_WEIGHTS_FOLDER] = opj(P[NETWORK_OUTPUT_FOLDER],'weights')
    P[WEIGHTS_FILE_PATH] = most_recent_file_in_folder(P[INITIAL_WEIGHTS_FOLDER],['net'],[])



#EOF