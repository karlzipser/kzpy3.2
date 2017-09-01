from Paths_Module import *
from All_Names_Module import *
exec(identify_file_str)

_ = dictionary_access



P = {}
P[SINGLE_VALUE_TOPICS] = [steer,state,motor,potential_collision,encoder,aruco_heading_x,aruco_heading_y,aruco_position_x,aruco_position_y,'cmd/heading_pause','cmd/car_in_range']
_(P,VERBOSE,equals,True)
_(P,EXAMPLE1,equals,False)
_(P,EXAMPLE2,equals,True)
_(P,EXAMPLE3,equals,False)
_(P,EXAMPLE4,equals,False)
_(P,MEO_PARAMS,equals,{acc_x:50,acc_y:50,acc_z:50,gyro_x:50,gyro_y:50,gyro_z:50,gyro_heading_x:50,gyro_heading_y:50,gyro_heading_z:50,encoder:200})

#P[DATASET_PATH] = opjm('ExtraDrive2/bdd_car_data_July2017_LCR')
#P[RUN_NAME] = 'direct_local_LCR_29Jul17_18h09m32s_Mr_Yellow'

#P[SRC] = opjm('rosbags/Mr_Yellow_29July2017/new')
#P[DST] = opjm('ExtraDrive2/bdd_car_data_July2017_LCR/h5py')

#EOF