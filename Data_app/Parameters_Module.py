from Paths_Module import *
#from All_Names_Module import *
exec(identify_file_str)


P = {}

P['SINGLE_VALUE_TOPICS'] = ['button_number', 'drive_mode', 'human_agent',  'steer','state','motor','potential_collision','encoder','aruco_heading_x','aruco_heading_y','aruco_position_x','aruco_position_y','cmd/heading_pause','cmd/car_in_range','cmd/steer','cmd/motor']

P['VECTOR3_TOPICS'] = ['acc','gyro','gps','gyro_heading','other_car_position']

P['STRING_TOPICS'] = ['behavioral_mode','place_choice']

P['MEO_PARAMS'] = {'acc_x':50,'acc_y':50,'acc_z':50,'gyro_x':50,'gyro_y':50,'gyro_z':50,'gyro_heading_x':50,'gyro_heading_y':50,'gyro_heading_z':50,'encoder':200}

P['USE_ARUCO'] = False


#EOF